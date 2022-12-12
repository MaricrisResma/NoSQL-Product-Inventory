
from djongo import models
from django import forms  

# Build Models and Forms here
class StockDetails(models.Model):
  creationDate = models.CharField(max_length=10)
  expiryDate = models.CharField(max_length=10)
  quantity = models.CharField(max_length=10)
  remaining = models.CharField(max_length=10)
  class Meta:
    abstract = True


class StockDetailsForm(forms.ModelForm):  
    class Meta:  
        model = StockDetails  # define the model the form wants to represent 
        fields = "__all__"  

class products(models.Model):
  productId = models.CharField(max_length=10)
  productName = models.CharField(max_length=10)
  productDescription = models.CharField(max_length=10)
  productCategory = models.CharField(max_length=10)
  price = models.CharField(max_length=10)
  totalStock = models.CharField(max_length=10)
  stockDetails = models.ArrayField(model_container=StockDetails)
  isOffered = models.CharField(max_length=10)

class productsForm(forms.ModelForm):  
    class Meta:  
        model = products  
        fields = "__all__"  

    
    
# https://www.djongomapper.com/using-django-with-mongodb-array-field/

# class Person(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)

# https://www.youtube.com/watch?v=VOddmV4Xl1g

# https://www.djongomapper.com/using-django-with-mongodb-array-field/4

# Daya edit para gumana ung embeddedfield model
# C:\Users\Makis\AppData\Local\Programs\Python\Python310\Lib\site-packages\djongo\models\fields.py

# Downgrade djongo due to bug in https://github.com/doableware/djongo/issues/566