from django.urls import path
from .import views, views_products

# In your urls file, you are not calling the view.<yourFunction> function, just listing a reference to it.
# Django then calls the function when a matching http request comes in and passes the HttpRequest object as a parameter by default.
# The request parameter is a HttpRequest object, which contains data about the request (see the docs for django 3.2).

urlpatterns = [
    # path('',views.index,name='index'),
    path('customer/add', views.cust_info), 
    path('customer/show',views.show_customers),  
    path('customer/edit/<str:emailAddress>', views.edit_customer),  
    path('customer/update/<str:emailAddress>', views.update_customer),  
    path('customer/delete/<str:emailAddress>', views.delete_customer),    

    path('product/add', views_products.prod_info), 
    path('product/show',views_products.show_products),  
    path('product/edit/<str:productId>', views_products.edit_product),  
    path('product/update/<str:productId>', views_products.update_product),  
    path('product/delete/<str:productId>', views_products.delete_product),    
    ]


