from django.shortcuts import render
from django.shortcuts import redirect
# from .models import Employee
import pymongo
# from django.conf import settings
from django.http import HttpResponse
import pymongo

DB_NAME = "jejomalu"
# Create your views here.
conn_str = "mongodb+srv://jejomalu:123jejomalu456@cluster0.0wvicuc.mongodb.net/test"
# conn_str = "mongodb+srv://Maricris:drowssap5MONGODB@cluster0.r4haknh.mongodb.net/?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(conn_str)
except Exception:
    print("Error:" + Exception)

myDb = client[DB_NAME]
# Create Customers collection
myCollection_Customers = myDb["customers"]

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
                'bStreet' : form['bStreet'],
                'bUnit' : form['bUnit'], 
                'bCity' : form['bCity'], 
                'bProvince' : form['bProvince'], 
                'bZip' : form['bZip'], 
                'bMobileNumber' : form['bMobileNumber']
            }, 
            'deliveryAddress' : 
            {
                'dStreet' : form['dStreet'], 
                'dUnit' : form['dUnit'], 
                'dCity' : form['dCity'], 
                'dProvince' : form['dProvince'], 
                'dZip' : form['dZip'],
                'dMobileNumber' : form['dMobileNumber']
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
    return render(request,'customer_add.html',{'form':form})  


def show_customers(request):
    customer_infos = []
    for customer_info in myCollection_Customers.find({}, {}):
        customer_infos.append(customer_info)
    return render(request,"customer_show.html",{'customer_infos':customer_infos})  

def edit_customer(request, emailAddress):  
    customer_info = myCollection_Customers.find_one({"emailAddress": emailAddress})  
    return render(request,'customer_edit.html', {'customer_info':customer_info})  

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
                'bStreet' : form['bStreet'],
                'bUnit' : form['bUnit'], 
                'bCity' : form['bCity'], 
                'bProvince' : form['bProvince'], 
                'bZip' : form['bZip'], 
                'bMobileNumber' : form['bMobileNumber']
            }, 
            'deliveryAddress' : 
            { 
                'dStreet' : form['dStreet'], 
                'dUnit' : form['dUnit'], 
                'dCity' : form['dCity'], 
                'dProvince' : form['dProvince'], 
                'dZip' : form['dZip'],
                'dMobileNumber' : form['dMobileNumber']
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

def get_top_5():
    pass

def get_low_5():
    pass

def get_expiry(range):
    pass

