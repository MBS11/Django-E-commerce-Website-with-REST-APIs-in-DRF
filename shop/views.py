from django.shortcuts import render
from .models import Product, Contact, Orders,OrderUpdate
from math import ceil
import json
from .serializers import ProductSerializer

# Create your views here.
from django.http import HttpResponse
import requests

def index(request): #to list products in Homepage 
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods} #Listing according to respective categories
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query,item):
    if query in item.disc.lower() or query in item.product_name.lower() or query in item.category.lower() :
        return True
    else:
        return False

def search(request): #to search any available product
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item) ]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) !=0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    if len(allProds)== 0 or len(query)<2 :
        params= {'msg': "Please make sure to enter relevent search query"}
    return render(request, 'shop/search.html', params)

def about(request): #for about us page
    return render(request, 'shop/about.html')

def contact(request):#To submit contact us queries
    thank=False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html', {'thank':thank})

def tracker(request): #To track an existing order placed by the user
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def prodView(request,myid): #to open and view the specific product
    product = Product.objects.filter(id=myid)

    stu=Product.objects.get(id=myid)
    serializer=ProductSerializer(stu)
    print(serializer.data)#To print the details of the product such as category,price,name etc using API when the user opens the specific product dashboard

    
    return render(request, 'shop/prodView.html',{'product':product[0]})

    

def checkout(request): #To place the order and Checkout
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json,name=name,amount=amount, email=email,address=address,city=city,state=state,zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html',{'thank': thank,'id': id})
    return render(request, 'shop/checkout.html')
