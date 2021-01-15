from rest_framework import serializers
from .models import *

#Serializers for different Models using ModelSerializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','product_name','category','subcategory','price','disc','pub_date','image']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orders
        fields=['order_id','name','email','address','amount','city','state','zip_code','phone','items_json']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=['msg_id','name','email','phone','desc']