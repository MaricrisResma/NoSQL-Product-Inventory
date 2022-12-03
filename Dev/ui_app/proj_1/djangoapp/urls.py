from django.urls import path
from .import views, views_products
urlpatterns = [
    # path('',views.index,name='index'),
    path('customer/add', views.cust_info), 
    path('customer/show',views.show_customers),  
    path('customer/edit/<str:emailAddress>', views.edit_customer),  
    path('customer/update/<str:emailAddress>', views.update_customer),  
    path('customer/delete/<str:emailAddress>', views.delete_customer),    

    path('product/add', views_products.prod_info), 
    path('product/show',views_products.show_products),  
    path('product/edit/<str:emailAddress>', views_products.edit_product),  
    path('product/update/<str:emailAddress>', views_products.update_product),  
    path('product/delete/<str:emailAddress>', views_products.delete_product),    
    ]
