from django.urls import path
from .import views
urlpatterns = [
    # path('',views.index,name='index'),
    path('customer/add', views.cust_info), 
    path('customer/show',views.show_customers),  
    path('customer/edit/<str:emailAddress>', views.edit_customer),  
    path('customer/update/<str:emailAddress>', views.update_customer),  
    path('customer/delete/<str:emailAddress>', views.delete_customer),    
    ]
