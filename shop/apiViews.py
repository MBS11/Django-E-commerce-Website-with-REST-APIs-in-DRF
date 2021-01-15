from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

#Using ModelViewSet for different Serializers
class ProductModelViewSet(viewsets.ModelViewSet): 
    queryset=Product.objects.all()
    serializer_class=ProductSerializer #Anyone Can Access

class OrderModelViewSet(viewsets.ModelViewSet):
    queryset=Orders.objects.all()
    serializer_class=OrderSerializer #Only Authorized user can access
    #Using Authentication $ Permissions
    authentication_classes=[BasicAuthentication] #Stating Authentication type
    permission_classes=[IsAuthenticated] #Stating Permission type

class ContactModelViewSet(viewsets.ModelViewSet):
    queryset=Contact.objects.all()
    serializer_class=ContactSerializer #Only Authorized user can access
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]