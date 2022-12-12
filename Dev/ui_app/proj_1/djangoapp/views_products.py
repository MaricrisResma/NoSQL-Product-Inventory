from django.shortcuts import render
from django.shortcuts import redirect
import pymongo
from django.conf import settings
from django.http import HttpResponse
import pymongo
from .import views
from .models import productsForm, StockDetailsForm, products
from datetime import date, datetime
from dateutil import parser

# Create your views here.
myDb = views.myDb
# Create Products collection
myCollection_Products = myDb["products"]

# Function called when adding a new product where it will check if there is form data first or not
# add_product
def prod_info(request):  
    # Upon next access is when the user clicks submit he is simply sending it back to the same URL now with method POST means with data info this FUNCTION which will be able to detect the method POST and begin to oarse data from the form and build the document to insert
    # HttpRequest.POST -  A dictionary-like object containing all given HTTP POST parameters, providing that the request contains form data
    if request.method == "POST": 
        form = request.POST
        print(form)

        format = "%Y-%m-%dT%H:%M" #https://www.freecodecamp.org/news/how-to-convert-a-string-to-a-datetime-object-in-python/
        creationDate = datetime.strptime(form['creationDate'], format)
        expiryDate = datetime.strptime(form['expiryDate'], format)

        # Here we manually render out a html form
        # form values are taken from POST httresponse once the user has submitted where it is taken from the tag name in the html
        product_info = { 
            'productId' : form['productId'],
            'productName' : form['productName'],
            'productDescription' : form['productDescription'],
            'productCategory' : form['productCategory'],
            'price' : float(form['price']),
            'totalStock' : int(form['remaining']), #totalstock at first is always equal to the remaining one
            'stockDetails' : #If it's the first time adding the product then for sure there will only be one stock first hence we hardcode the array as only having 1 element at first creation
                 [
                { 
                'creationDate' : creationDate,
                'expiryDate' : expiryDate,
                'quantity' : int(form['quantity']),
                'remaining' : int(form['remaining']) 
                },
                 ],
            'isOffered' : form['isOffered']  
        } 

        myCollection_Products.insert_one(product_info)
        return redirect('/product/show/all')  #If you addded a new product you are automatically redirected to the product summary

    else:  
        form = {
        }

    # The first access to the URL with no POST data it will submit a blank form
    return render(request,'product_add.html',{'form':form})   

# URL will call this function that will find  all prod documents from the collection and input to render to the corresponding show html
def show_products(request):   
    product_infos = []
    ExpiredFilter = {}
    myQueryDict = {}

    if request.GET.get('getExpired') == 'getExpired':
            print("getExpired clicked!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(type(datetime.now()))
            ExpiredFilter = {'stockDetails':{'expiryDate': {'$lte':datetime.now()}}} #not working :()
            myQueryDict.update(ExpiredFilter)

    # Accessing with filter inputs
    if request.method == "POST"  :
        form = request.POST
        print(form)
        productNameFilter = {}
        productDescriptionFilter = {}
        productCategoryFilter = {}
        totalStockFilter = {} 
        ExpiredFilter = {}

        if form['productNameFilter'] != '': 
            productNameFilter = {'productName': {'$regex':form['productNameFilter'], '$options' : 'i'}}
            myQueryDict.update(productNameFilter)

        if form['productDescriptionFilter'] != '': 
            productDescriptionFilter = {'productDescription': {'$regex':form['productDescriptionFilter'], '$options' : 'i'}}
            myQueryDict.update(productDescriptionFilter)

        if form['productCategory'] != '': #
            productCategoryFilter = {'productCategory': {'$regex':form['productCategory'], '$options' : 'i'}}
            myQueryDict.update(productCategoryFilter)

        if form['totalStockFilter'] != '': 
            totalStockFilter = {'totalStock': {'$lte':int(form['totalStockFilter'])}}
            myQueryDict.update(totalStockFilter)
        
        # myQueryDict = {'productName': productNameFilter, 'productDescription': productDescriptionFilter, 'productCategory': productCategoryFilter, 'totalStock': totalStockFilter, 'stockDetails': ExpiredFilter}
        # {productName: {$regex:'che', '$options' : 'i'},productDescription: {$regex:'br', '$options' : 'i'}, productCategory: {$regex:'br', '$options' : 'i'}, totalStock: {$lte:15}}
        
        print(myQueryDict)
        for product_info in myCollection_Products.find(myQueryDict):
            product_infos.append(product_info)
    
    # Access first time no filter so just get all {}
    else:

        for product_info in myCollection_Products.find({}, {}):
            product_infos.append(product_info)
        
    # render() Combines a given html template with a given context dictionary and \
    # returns an HttpResponse object with that rendered text built in the template for the UI display
    return render(request,"product_show_all.html",{'product_infos':product_infos})  

# edit URL will call this function that will 
def edit_product(request, productId):  
    product_info = myCollection_Products.find_one({"productId": productId})  
    return render(request,'product_edit.html', {'product_info':product_info})   

def update_product(request, productId):  
    form = request.POST
    format = "%Y-%m-%dT%H:%M" #https://www.freecodecamp.org/news/how-to-convert-a-string-to-a-datetime-object-in-python/
    creationDate = datetime.strptime(form['creationDate'], format)
    expiryDate = datetime.strptime(form['expiryDate'], format)
    product_new = {  
        "$set": 
        { 
            'productId' : form['productId'],
            'productName' : form['productName'],
            'productDescription' : form['productDescription'],
            'productCategory' : form['productCategory'],
            'price' : float(form['price']), 
            'totalStock' : int(form['remaining']), #At edit reset should always be same as remaining
            'stockDetails' : 
                [
                { 
                'creationDate' : creationDate,
                'expiryDate' : expiryDate,
                'quantity' : int(form['quantity']),
                'remaining' : int(form['remaining']) 
                },
                ],
            'isOffered' : form['isOffered']  
        } 
    }
    myCollection_Products.update_one({"productId": productId}, product_new)
    return redirect('/product/show/all')  

def delete_product(request, productId):  
    product = myCollection_Products.delete_one({"productId": productId})
    return redirect("/product/show/all")  

# Note: Developer realized models cant be used because database in settings still needs to be done when extracting data from  mongodb
def show_product(request, productId):

    # POST when adding stock element
    if request.method == "POST": 
        form = request.POST

        format = "%Y-%m-%dT%H:%M"
        newcreationDate = datetime.strptime(form['newcreationDate'], format)
        newexpiryDate = datetime.strptime(form['newexpiryDate'], format)

        newStock = { 
                    'creationDate' : newcreationDate,
                    'expiryDate' : newexpiryDate,
                    'quantity' : int(form['newquantity']),
                    'remaining' : int(form['newremaining']) 
                    }
        
        #Update the array of stockDetails element 
        myCollection_Products.update_one(
            {'productId': productId}, 
            {'$push': 
                {'stockDetails': newStock}
            }
        )

        # Compute total Stock
        # https://www.tutorialspoint.com/how-to-sum-every-field-in-a-sub-document-of-mongodb        
        myPipeline =  [
                        {'$match': 
                            {'productId':productId}
                        },
                        {'$unwind': "$stockDetails" },
                        {'$group': 
                            {
                                '_id': '$_id', 
                                'productId': {'$first': '$productId'}, 
                                'totalStock': {'$sum': '$stockDetails.remaining'}
                            }  
                        }
                    ] 
        myAggGroup = myCollection_Products.aggregate(myPipeline)
        myAggGroupList = list(myAggGroup)
        updatedTotalStock = myAggGroupList[0]['totalStock']

        # Update the totalStock element after adding new stock
        product_elem_new = {  
            "$set": 
            { 
                'totalStock' : updatedTotalStock,
            } 
        }
        
        myCollection_Products.update_one({"productId": productId}, product_elem_new)

    #If this is just to show the product as redirected with url and not coming from post submission of new stock (POST)
    else: 
        pass
    
    product_info = myCollection_Products.find_one({"productId": productId})
    # Need to convert to string so that the show will show in YY-MM-DD format
    stockDetailsArray = product_info['stockDetails']
    for elem in stockDetailsArray:
        elem['creationDate'] = str(elem['creationDate'])
        elem['expiryDate'] = str(elem['expiryDate'])

    return render(request,'product_show.html', {'product_info':product_info})   

def remove_product_stock(request, productId, creationDate):
    product_info = myCollection_Products.find_one({"productId": productId})  
    stockDetailsArray = product_info['stockDetails']

    # Remove the stock that matches the creation date (workaround than pull because the creationdate hard to match)
    for elem in stockDetailsArray:
        if str(elem['creationDate']) == creationDate:
            stockDetailsArray.remove(elem)
            product_info['stockDetails'] = stockDetailsArray 
            
            #Update the array of stockDetailselement
            product_elem_new = {  
                "$set": 
                { 
                    'stockDetails' : stockDetailsArray
                } 
            }
            myCollection_Products.update_one({"productId": productId}, product_elem_new)

    # # Remove an element / hard to match elem match with date format :(
    # myCollection_Products.update_one(
    #         {'productId': productId}, 
    #         {'$pull': 
    #             {'stockDetails': 
    #                 {'$elemMatch': 
    #                     {'creationDate': creationDate}
    #                 }
    #             }
    #         }
    #     )
    # https://www.tutorialspoint.com/how-to-sum-every-field-in-a-sub-document-of-mongodb  
    # Compute total Stock
    myPipeline =  [
                        {'$match': 
                            {'productId':productId}
                        },
                        {'$unwind': "$stockDetails" },
                        {'$group': 
                            {
                                '_id': '$_id', 
                                'productId': {'$first': '$productId'}, 
                                'totalStock': {'$sum': '$stockDetails.remaining'}
                            }  
                        }
                    ] 
    myAggGroup = myCollection_Products.aggregate(myPipeline)
    myAggGroupList = list(myAggGroup)

    if myAggGroupList != []:
        updatedTotalStock = myAggGroupList[0]['totalStock']
    else:
        updatedTotalStock = 0

        # Update the totalStock element after adding new stock
    product_elem_new = {  
            "$set": 
            { 
                'totalStock' : updatedTotalStock,
            } 
        }
        
    myCollection_Products.update_one({"productId": productId}, product_elem_new)
        
    url = "/product/show/"+ productId
    return redirect(url)  

def add_stock_product(request, productId):
    product_info = myCollection_Products.find_one({"productId": productId})
    # The first access to the URL with no POST data it will submit a blank form
    return render(request,'product_stock_add.html',{'product_info':product_info})   













# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#  Syntax Experiments
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # https://www.programiz.com/python-programming/examples/string-to-datetime#:~:text=Using%20strptime()%20%2C%20date%20and,or%20date%20or%20time%20individually.    
    
    # print("*************************************************************************")
    # print(product_info)
    # print("---------------------------------------")
    # print(type(creationDate))
    # print(creationDate)
    # print("---------------------------------------")
    # print(((product_info['stockDetails'])[0])['creationDate'])
    # # print(type(((product_info['stockDetails'])[0])['creationDate']))
    # print("*************************************************************************")

    # Here we practice using djongo model at least to get data as array field

def old_remove_product_stock(request, productId, creationDate):
    product_info = myCollection_Products.find_one({"productId": productId})  
    # stockDetailsArray = product_info['stockDetails']
    # updatedTotalStock =  product_info['totalStock']
    # print(type(creationDate))
    # format = "%Y-%m-%d %H:%M:%S" #https://www.freecodecamp.org/news/how-to-convert-a-string-to-a-datetime-object-in-python/
    # creationDate = datetime.strptime(creationDate, format) #TODO verify if thhis works!!!!
    # print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    # print(type(creationDate))

    # # Remove the stock that matches the creation date
    # for elem in stockDetailsArray:
    #     if str(elem['creationDate']) == creationDate:
    #         updatedTotalStock = updatedTotalStock - elem['remaining']
    #         stockDetailsArray.remove(elem)
    #         product_info['stockDetails'] = stockDetailsArray 
            
    #         #Update the array of stockDetailselement
    #         product_elem_new = {  
    #             "$set": 
    #             { 
    #                 'totalStock' : updatedTotalStock,
    #                 'stockDetails' : stockDetailsArray
    #             } 
    #         }
    #         myCollection_Products.update_one({"productId": productId}, product_elem_new)

    # Remove an element
    myCollection_Products.update_one(
            {'productId': productId}, 
            {'$pull': 
                {'stockDetails': 
                    {'$elemMatch': 
                        {'creationDate': creationDate}
                    }
                }
            }
        )
    # https://www.tutorialspoint.com/how-to-sum-every-field-in-a-sub-document-of-mongodb     
    # Compute total Stock
    myPipeline =  [
                        {'$match': 
                            {'productId':productId}
                        },
                        {'$unwind': "$stockDetails" },
                        {'$group': 
                            {
                                '_id': '$_id', 
                                'productId': {'$first': '$productId'}, 
                                'totalStock': {'$sum': '$stockDetails.remaining'}
                            }  
                        }
                    ] 
    myAggGroup = myCollection_Products.aggregate(myPipeline)
    myAggGroupList = list(myAggGroup)
    print(myAggGroupList) 
        # [{'_id': ObjectId('63918fac5a3a753879383892'), 
        #                         'productId': '5550', 
        #                         'totalStock': 42}]
        
    updatedTotalStock = myAggGroupList[0]['totalStock']

        # Update the totalStock element after adding new stock
    product_elem_new = {  
            "$set": 
            { 
                'totalStock' : updatedTotalStock,
            } 
        }
        
    myCollection_Products.update_one({"productId": productId}, product_elem_new)
        
    url = "/product/show/"+ productId
    return redirect(url)  

def index_test(request):
    form = productsForm()

    if request.method == 'POST':
        # print(request.POST)
        form = productsForm(request.POST)
        print(form['stockDetails'])

        if form.is_valid():
            form = request.POST
            product_info = { 
                'productId' : form['productId'],
                'productName' : form['productName'],
                'productDescription' : form['productDescription'],
                'productCategory' : form['productCategory'],
                'price' : form['price'],
                'totalStock' : form['totalStock'],
                'stockDetails' : 
                    [
                    {   
                    'creationDate' : form['stockDetails-0-creationDate'],
                    'expiryDate' : form['stockDetails-0-expiryDate'],
                    'quantity' : form['stockDetails-0-quantity'],
                    'remaining' : form['stockDetails-0-remaining'] 
                    },
                    ],
                'isOffered' : form['isOffered']  
            } 
            print(product_info)
            myCollection_Products.insert_one(product_info)

    context = {'form':form}
    return render(request, 'index_test.html', context)