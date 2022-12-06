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
myCollection_Products = myDb["products"]

# Function called when adding a new product where it will check if there is form data first or not
def prod_info(request):  
    creationDatevar = str('creationDate')
    # Upon next access is when the user clicks submit he is simply sending it back to the same URL now with method POST means with data info this FUNCTION which will be able to detect the method POST and begin to oarse data from the form and build the document to insert
    # HttpRequest.POST -  A dictionary-like object containing all given HTTP POST parameters, providing that the request contains form data
    if request.method == "POST": 
        form = request.POST
        print(form)
        # Here we manually render out a html form
        # form values are taken from POST httresponse once the user has submitted where it is taken from the tag name in the html
        product_info = { 
            'productId' : form['productId'],
            'productName' : form['productName'],
            'productDescription' : form['productDescription'],
            'productCategory' : form['productCategory'],
            'price' : form['price'],
            'totalStock' : form['totalStock'],
            'stockDetails' : 
                # [
                { 
                creationDatevar : form[creationDatevar],
                'expiryDate' : form['expiryDate'],
                'quantity' : form['quantity'],
                'remaining' : form['remaining'] 
                },
                # ],
            'isOffered' : form['isOffered']  
        } 

        print(product_info)
        myCollection_Products.insert_one(product_info)
        return redirect('/product/show')  #If you addded a new product you are automatically redirected to the product summary

    else:  
        form = {
        }

    # The first access to the URL with no POST data it will submit a blank form
    return render(request,'product_add.html',{'form':form})  

# URL will call this function that will find  all prod documents from the collection and input to render to the corresponding show html
def show_products(request):   
    product_infos = []
    for product_info in myCollection_Products.find({}, {}):
        product_infos.append(product_info)
    # render() Combines a given html template with a given context dictionary and \
    # returns an HttpResponse object with that rendered text built in the template for the UI display
    return render(request,"product_show.html",{'product_infos':product_infos})  

# edit URL will call this function that will 
def edit_product(request, productId):  
    product_info = myCollection_Products.find_one({"productId": productId})  
    return render(request,'product_edit.html', {'product_info':product_info})   

def update_product(request, productId):  
    
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
                # [
                { 
                'creationDate' : form['creationDate'],
                'expiryDate' : form['expiryDate'],
                'quantity' : form['quantity'],
                'remaining' : form['remaining'] 
                },
                # ],
            'isOffered' : form['isOffered']  
        } 
    }
    myCollection_Products.update_one({"productId": productId}, product_new)
    return redirect('/product/show')  

def delete_product(request, productId):  
    employee = myCollection_Products.delete_one({"productId": productId})
    return redirect("/product/show")  

def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

def get_top_5():
    pass

def get_low_5():
    pass

def get_expiry(range):
    pass

