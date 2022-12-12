from django.shortcuts import render
from django.shortcuts import redirect
import pymongo
from django.conf import settings
from django.http import HttpResponse
import pymongo
from .import views
# import views as views
# Create your views here.
myDb = views.myDb
# # Step 4: create a collection

myCollection_orders = myDb["orders"]



def orders_info(request):  
    if request.method == "POST":

        # To do get collection for products and update the stock
        #   
        form = request.POST
        print(form)
        orders_info = {

            'emailAddress' : form['emailAddress'],
            'orderId' : form['orderId'],
            'employeeUserName' : form['employeeUserName'], 
          
            'deliveryAddress' : 
                { 
                'dName' : form ['dName'],
                'dStreet' : form['dStreet'], 
                'dCity' : form['dCity'], 
                'dProvince' : form['dProvince'], 
                'dZip' : form['dZip'], 
                'dMobileNumber' : form['dMobileNumber']
                }, 

            'billingAddress' :
                { 
                'bName' : form ['bName'], 
                'bStreet' : form ['bStreet'], 
                'bCity' : form ['bCity'], 
                'bProvince' : form ['bProvince'], 
                'bZip' : form ['bZip'], 
                'bMobileNumber' : form ['bMobileNumber' ]
                }, 
   
            'paymentMethod' : 
                { 
                'paymentType' : form['paymentType'], 
                'cardScheme' : form['cardScheme'], 
                'cardLast4' : form['cardLast4'] 
                },
                
            'totalQty' : form['totalQty'], 
            'orderTotal' : form['orderTotal'], 
            'grossTotal' : form['grossTotal'], 
            'tax' : form['tax'], 
            'deliveryFee' : form['deliveryFee'],
                
            'orderDetails' : [
                {
                'productId': form['productId'],
                'productName': form['productName'],
                'quantity': form['quantity'],
                'price': form['price'],
                'subTotal': form['subTotal']
                },
            ],
                
            'orderDate' : form['orderDate'], 
            'orderStatus' : form['orderStatus'], 
            'statusDate' : form['statusDate'], 
        }


        print(orders_info)
        myCollection_orders.insert_one(orders_info)
        return redirect('/order/show/all')  
    else:  
        form = {
        }
    return render(request,'order_add.html',{'form':form})  


def show_orders(request):
    orders_infos = []
    for orders_info in myCollection_orders.find({}, {}):
        orders_infos.append(orders_info)
    return render(request,"order_show_all.html",{'orders_infos':orders_infos})  


def show_order(request, orderId):
    orders_info = myCollection_orders.find_one({"orderId": orderId})
    print(orders_info)  
    return render(request,"order_show.html",{'orders_info':orders_info})  

def edit_orders(request, emailAddress):  
    orders_info = myCollection_orders.find_one({"emailAddress": emailAddress})  
    return render(request,'order_edit.html', {'orders_info':orders_info})  

def update_orders(request, emailAddress):  
    
    form = request.POST
    orders_new = {  
        "$set": 
            {
            'emailAddress' : form['emailAddress'],
            'orderId' : form['orderId'],
            'employeeUserName' : form['employeeUserName'], 
            'deliveryAddress' : 
                { 
                'dName' : form ['dName'],
                'dStreet' : form ['dStreet'], 
                'dCity' : form ['dCity'], 
                'dProvince' : form ['dProvince'], 
                'dZip' : form ['dZip'], 
                'dMobileNumber' : form ['dMobileNumber']
                }, 

            'billingAddress' :
                { 
                'bName' : form ['bName'], 
                'bStreet' : form ['bStreet'], 
                'bCity' : form ['bCity'], 
                'bProvince' : form['bProvince'], 
                'bZip' : form['bZip'], 
                'bMobileNumber' : form['bMobileNumber']
                }, 

            'paymentMethod' : 
                { 
                'paymentType' : form['paymentType'], 
                'cardScheme' : form['cardScheme'], 
                'cardLast4' : form['cardLast4'] ,
                },
             
            'totalQty' : form['totalQty'], 
            'orderTotal' : form['orderTotal'], 
            'grossTotal' : form['grossTotal'], 
            'tax' : form['tax'], 
            'deliveryFee' : form['deliveryFee'], 
            
            'orderDetails' : 
                [
                    {
                    'productId': form['productId'],
                    'productName': form['productName'],
                    'quantity': form['quantity'],
                    'price': form['price'],
                    'subTotal': form['subTotal']
                    },
                ],

            'orderDate' : form['orderDate'], 
            'orderStatus' : form['orderStatus'], 
            'statusDate' : form['statusDate'], 
        }
    }
    myCollection_orders.update_one({"emailAddress": emailAddress}, orders_new)
    return redirect('/order/show/all')  

def delete_orders(request, orderId):  
    order = myCollection_orders.delete_one({"orderId": orderId})
    return redirect("/order/show/all")  

def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

def get_top_5():
    pass

def get_low_5():
    pass

def get_expiry(range):
    pass
