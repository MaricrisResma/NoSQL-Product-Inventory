from django.shortcuts import render
from django.shortcuts import redirect
# from .models import Employee
import json
import pymongo
from django.conf import settings
from django.http import HttpResponse
import pymongo
# import views as views
from .import views
from datetime import date, datetime
from dateutil import parser


# Create your views here.


myDb = views.myDb
# # Step 4: create a collection
# myCollection_Products = myDb["reviews"]
myCollection_reviews = myDb["reviews"]


def reviews_info(request):  
    if request.method == "POST":  
        form = request.POST
        print(form)
        
        reviews_info = {
            'productId' : form['productId'],                  
            'reviewDetails' :
            [
                  {
                  'reviewID' : form['reviewId'],
                  'orderId' : form['orderId'],
                  'postDate' : form ['postDate'],
                  'rating' : int(form['rating']),
                  'reviewText' : form ['reviewText'],
                  'emailAddress' : form['emailAddress'],
                  },             
            ],   
            'ratingCount' : int(form['ratingCount']),
            'totalRatings' : int(form['totalRatings'])
        }           
                  
        print(reviews_info)
        myCollection_reviews.insert_one(reviews_info)
        return redirect('/review/show/all')  
    else:  
        form = {
        }
    return render(request,'review_add.html',{'form':form})  

def show_reviews(request):
    # rrmsg': '$group: is not allowed or the syntax is incorrect, see the Atlas documentation for more information', 'code': 8000, 'codeName': 'AtlasError'}
    # myPipeline = [
    #     {'$unwind': "$reviewDetails" },
    #     {'$group:':
    #         {
    #         '_id': '$_id', 
    #         'productId': {'$first': '$productId'}, 

    #         }
    #     }
    # ]

    # myAggProject = myCollection_reviews.aggregate(myPipeline)
    # myAggProjectList = list(myAggProject)

    # print[myAggProjectList]

    reviews_infos = [] #Will contain all the myAggProject
    # for reviews_info in myAggProject:
    #     reviews_infos.append(reviews_info)

    # workaroudn do computation in python
    for reviews_info in myCollection_reviews.find({}, {}):
        totalRating = 0
        lenReviewDetailsArray = len(reviews_info['reviewDetails'])
        print("----------------------------------------->", lenReviewDetailsArray)
        for reviewDetails in reviews_info['reviewDetails']:
            print("------------------------------------------", reviewDetails['rating'])
            totalRating = totalRating + reviewDetails['rating']
            print("------------------------------------------TOTAL", reviewDetails['rating'])
           
        avgRating = totalRating/lenReviewDetailsArray
        reviews_info.update( {'avgRating' : avgRating} )
        reviews_infos.append(reviews_info)


    return render(request,"review_show_all.html",{'reviews_infos':reviews_infos})  

def show_reviews_byId(request):
    reviews_infos = [] #Will contain all the myAggProject

    for reviews_info in myCollection_reviews.find({}, {}):
        reviews_infos.append(reviews_info)

    return render(request,"review_show_all_reviewId.html",{'reviews_infos':reviews_infos})  


def show_product_reviews(request, productId):
    # reviews_info = myCollection_reviews.find_one({"productId": productId})
    # reviewDetailsArray = reviews_info['reviewDetails']

    # POST when adding a new review for the product
    if request.method == "POST": 
        form = request.POST

        format = "%Y-%m-%dT%H:%M"
        newpostDate = datetime.strptime(form['postDate'], format)

        newReview = { 
            'reviewId' : form['reviewId'],
            'orderId' : form['orderId'],
            'postDate' : newpostDate,
            'rating' : int(form['postDate']),
            'reviewText' : form['reviewText'],
            'emailAddress' : form['emailAddress']
            } 
                                
        # Add it to the array
        # reviewDetailsArray.append(newReview)

        # product_elem_new = {  
        #     "$set": 
        #     { 
        #         'reviewDetails' : reviewDetailsArray
        #     } 
        # }

        myCollection_reviews.update(
            {'productId': productId}, 
            {'$push': 
                {'reviewDetails': newReview}
            }
        )

        # myCollection_reviews.update_one({"productId": productId}, product_elem_new)
        # reviews_info = myCollection_reviews.find_one({"productId": productId})
        # aggregation to pass the value of updated average rating etc...
        # Update the array of stockDetails element

    #If this is just to show the product as redirected with url and not coming from post submission of new stock (POST)
    else: 
        pass

    reviews_info = myCollection_reviews.find_one({"productId": productId})
    # Need to convert to string so that the show will show in YY-MM-DD format
    reviewDetailsArray = reviews_info['reviewDetails']
    for elem in reviewDetailsArray:
        elem['postDate'] = str(elem['postDate'])

    return render(request,'review_show.html', {'reviews_info':reviews_info})   

# def edit_reviews(request, productId):  
#     reviews_info = myCollection_reviews.find_one({"productId": productId})  
#     return render(request,'review_edit.html', {'reviews_info':reviews_info})  

# def update_reviews(request, productId):  
    
#     form = request.POST
#     reviews_new = {  
#         "$set": 
#             {
#             'productId' : form['productId'],                  
#             'reviewDetails' :
#             [
#                 {
#                   'reviewID' : form['reviewId'],
#                   'orderId' : form['orderId'],
#                   'postDate' : form ['postDate'],
#                   'rating' : int(form['rating']),
#                   'reviewText' : form ['reviewText'],
#                   'emailAddress' : form['emailAddress'],
#                   },    
#             ],              
#             'ratingCount' : int(form['ratingCount']),
#             'totalRatings' : int(form['totalRatings'])
#         }    
#         }
    
#     myCollection_reviews.update_one({"productId": productId}, reviews_new)
#     return redirect('/review/show/all')  

def delete_reviews(request, productId):  
    employee = myCollection_reviews.delete_one({"productId": productId})
    return redirect("/review/show/all")  

def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

def get_top_5():
    pass

def get_low_5():
    pass

def get_expiry(range):
    pass
