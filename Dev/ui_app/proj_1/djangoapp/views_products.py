from django.shortcuts import render
from django.shortcuts import redirect
import pymongo
from django.conf import settings
from django.http import HttpResponse
import pymongo
from .import views

# Create your views here.
myDb = views.myDb
# Create Products collection
myCollection_Products = myDb["Products"]

def prod_info(request):  
    if request.method == "POST":  
        form = request.POST
        print(form)
        product_info = { 
            'productId' : form['productId'],
            'productName' : form['productId'],
            'productDescription' : form['productDescription'],
            'productCategory' : form['productCategory'],
            'price' : form['price'],
            'totalStock' : form['totalStock'],
            'stockDetails' : 
                { 
                'creationDate' : form['creationDate'],
                'expiryDate' : form['expiryDate'],
                'quantity' : form['quantity'],
                'remaining' : form['remaining'] 
                },
            'isOffered' : form['isOffered']  
        } 

        print(product_info)
        myCollection_Products.insert_one(product_info)
        return redirect('/product/show')  
    else:  
        form = {
        }
    return render(request,'add.html',{'form':form})  


def show_products(request):
    product_infos = []
    for product_info in myCollection_Products.find({}, {}):
        product_infos.append(product_info)
    return render(request,"show.html",{'product_infos':product_infos})  

def edit_product(request, emailAddress):  
    product_info = myCollection_Products.find_one({"emailAddress": emailAddress})  
    return render(request,'edit.html', {'product_info':product_info})  

def update_product(request, emailAddress):  
    
    form = request.POST
    product_new = {  
        "$set": 
        { 
            'productId' : form['productId'],
            'productName' : form['productId'],
            'productDescription' : form['productDescription'],
            'productCategory' : form['productCategory'],
            'price' : form['price'],
            'totalStock' : form['totalStock'],
            'stockDetails' : 
                { 
                'creationDate' : form['creationDate'],
                'expiryDate' : form['expiryDate'],
                'quantity' : form['quantity'],
                'remaining' : form['remaining'] 
                },
            'isOffered' : form['isOffered']  
        } 
    }
    myCollection_Products.update_one({"emailAddress": emailAddress}, product_new)
    return redirect('/product/show')  

def delete_product(request, emailAddress):  
    employee = myCollection_Products.delete_one({"emailAddress": emailAddress})
    return redirect("/product/show")  

def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

def get_top_5():
    pass

def get_low_5():
    pass

def get_expiry(range):
    pass

