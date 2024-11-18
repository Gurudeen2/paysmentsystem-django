from django.urls import path
from . import views
urlpatterns =[
    path('<int:id>', views.attotcart, name='addtocart' ),
    path('cart', views.singlecart, name='carts'),
    path('delete/<int:id>', views.deletecart, name='deletecart'),
]