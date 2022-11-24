from django.shortcuts import render
from django.shortcuts import redirect
# from .models import Employee
import json
import pymongo
from django.conf import settings
from django.http import HttpResponse
import pymongo

# Create your views here.
conn_str = "mongodb+srv://Maricris:drowssap5MONGODB@cluster0.r4haknh.mongodb.net/?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(conn_str)
except Exception:
    print("Error:" + Exception)

#Step3
myDb = client["Firstdb"]
# # Step 4: create a collection
myCollection_Products = myDb["Products"]
myCollection_Customers = myDb["Customers"]

def cust_info(request):  
    if request.method == "POST":  
        form = request.POST
        print(form)
        customer_info = {
            'emailAddress' : form['emailAddress'], 
            'firstName' : form['firstName'], 
            'lastName' : form['lastName'], 
            'billingAddress' :
                { 
                'bstreet' : form['bstreet'], 
                'bcity' : form['bcity'], 
                'bprovince' : form['bprovince'], 
                'bzip' : form['bzip'], 
                'bmobileNumber' : form['bmobileNumber' ]
                }, 
            'deliveryAddress' : 
                { 
                'street' : form['street'], 
                'city' : form['city'], 
                'province' : form['province'], 
                'zip' : form['zip'], 
                'mobileNumber' : form['mobileNumber']
                }, 
            'paymentMethod' : 
                { 
                'paymentType' : form['paymentType'], 
                'nameOnCard' : form['nameOnCard'], 
                'cardScheme' : form['cardScheme'], 
                'cardLast4' : form['cardLast4'], 
                'cardExpiryDate' : form['cardExpiryDate']
                } 
        }
        print(customer_info)
        myCollection_Customers.insert_one(customer_info)
        return redirect('/customer/show')  
    else:  
        form = {
        }
    return render(request,'add.html',{'form':form})  


def show_customers(request):
    customer_infos = []
    for customer_info in myCollection_Customers.find({}, {}):
        customer_infos.append(customer_info)
    return render(request,"show.html",{'customer_infos':customer_infos})  

def edit_customer(request, emailAddress):  
    customer_info = myCollection_Customers.find_one({"emailAddress": emailAddress})  
    return render(request,'edit.html', {'customer_info':customer_info})  

def update_customer(request, emailAddress):  
    
    form = request.POST
    customer_new = {  
        "$set": 
            {
            'emailAddress' : form['emailAddress'], 
            'firstName' : form['firstName'], 
            'lastName' : form['lastName'], 
            'billingAddress' :
                { 
                'bstreet' : form['bstreet'], 
                'bcity' : form['bcity'], 
                'bprovince' : form['bprovince'], 
                'bzip' : form['bzip'], 
                'bmobileNumber' : form['bmobileNumber' ]
                }, 
            'deliveryAddress' : 
                { 
                'street' : form['street'], 
                'city' : form['city'], 
                'province' : form['province'], 
                'zip' : form['zip'], 
                'mobileNumber' : form['mobileNumber']
                }, 
            'paymentMethod' : 
                { 
                'paymentType' : form['paymentType'], 
                'nameOnCard' : form['nameOnCard'], 
                'cardScheme' : form['cardScheme'], 
                'cardLast4' : form['cardLast4'], 
                'cardExpiryDate' : form['cardExpiryDate']
                } 
        }
    }
    myCollection_Customers.update_one({"emailAddress": emailAddress}, customer_new)
    return redirect('/customer/show')  

def delete_customer(request, emailAddress):  
    employee = myCollection_Customers.delete_one({"emailAddress": emailAddress})
    return redirect("/customer/show")  

def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

