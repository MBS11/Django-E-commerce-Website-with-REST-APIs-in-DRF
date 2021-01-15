
from django.urls import path,include
from . import views
from . import apiViews
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
#Using router for various URLs of APIs
router.register('Product-api', apiViews.ProductModelViewSet,basename='product')
router.register('Order-api', apiViews.OrderModelViewSet,basename='order')
router.register('ContactUs-api', apiViews.ContactModelViewSet,basename='contact')



urlpatterns = [
    path("", views.index , name="ShopHome"),
    path("about/", views.about , name="AboutUs"),
    path("contact/", views.contact , name="ContactUs"),
    path("tracker/", views.tracker , name="TrackingStatus"),
    path("search/", views.search , name="Search"),
    path("products/<int:myid>", views.prodView , name="ProductView"),
    path("checkout/", views.checkout , name="Checkout"),
    path('api/',include(router.urls)),
]