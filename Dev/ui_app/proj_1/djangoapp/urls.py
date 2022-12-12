from django.urls import include, path
from datetime import date, datetime
from .import views, views_products, views_orders, views_reviews

# In your urls file, you are not calling the view.<yourFunction> function, just listing a reference to it.
# Django then calls the function when a matching http request comes in and passes the HttpRequest object as a parameter by default.
# The request parameter is a HttpRequest object, which contains data about the request (see the docs for django 3.2).

urlpatterns = [

    # url customer
    path('',views.index,name='index'),
    # path('test',views_products.index_test,name='index_test'),
    path('customer/add', views.cust_info), 
    path('customer/show/all', views.show_customers),  
    path('customer/show/<str:emailAddress>', views.show_customer_detail), 
    path('customer/edit/<str:emailAddress>', views.edit_customer),  
    path('customer/update/<str:emailAddress>', views.update_customer),  
    path('customer/delete/<str:emailAddress>', views.delete_customer),    

    # url product 
    path('product/add', views_products.prod_info), 
    path('product/show/all',views_products.show_products),  
    path('product/show/<str:productId>',views_products.show_product),
    path('product/show/<str:productId>/add-stock',views_products.add_stock_product),
    path('product/show/<str:productId>/remove-stock/<str:creationDate>',views_products.remove_product_stock),
    path('product/edit/<str:productId>', views_products.edit_product),  
    path('product/update/<str:productId>', views_products.update_product),  
    path('product/delete/<str:productId>', views_products.delete_product),    

    # url order
    path('order/add', views_orders.orders_info), 
    path('order/show/all',views_orders.show_orders),  
    path('order/show/<str:orderId>',views_orders.show_order),  
    # path('order/edit/<str:orderId>', views_orders.edit_orders),  
    # path('order/update/<str:orderId>', views_orders.update_orders),  
    path('order/delete/<str:orderId>', views_orders.delete_orders),


    # url reviews
    path('customer/addReview/<str:emailAddress>', views.add_review), 
    path('review/show/all', views_reviews.show_reviews),  
    path('review/show/all-reviewIds', views_reviews.show_reviews_byId),  
    path('review/show/<str:productId>',views_reviews.show_product_reviews),
    # path('review/edit/<str:reviewId>', views_reviews.edit_reviews),  
    # path('review/update/<str:reviewId>', views_reviews.update_reviews),  
    path('review/delete/<str:productId>', views_reviews.delete_reviews),  

    ]


    



