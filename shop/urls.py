from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="AboutUs"),
    path("contact/",views.contact,name="ContactUs"),
    path("tracker/",views.tracker,name="TrackingStatus"),
    path("search/",views.search,name="Search"),
    path("products/<int:myid>",views.productView,name="Productview"), #urls is getting myid from quickview in index.html
    path("checkout/",views.checkout,name="Checkout"),
    path("handlerequest/",views.handlerequest,name="HandleRequest")
]