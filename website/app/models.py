from django.db import models
import os
import datetime
from django.contrib.auth.models import User

# Create your models here.
def getfilename(request,filename):
    now_time=datetime.datetime.now().strftime("%y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads',new_filename)
class Catagories(models.Model):
    name=models.CharField(max_length=150,null=True,blank=True)
    image=models.ImageField(upload_to=getfilename, height_field=None, width_field=None, max_length=None,null=True,blank=True)
    description=models.TextField(max_length=500,null=False)
    status=models.BooleanField(default=False,help_text="0-default,1-hidden")
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    catagories=models.ForeignKey(Catagories, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=150,null=True,blank=True)
    vendor=models.CharField( max_length=50,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    old_price=models.FloatField(null=False,blank=False)
    new_price=models.FloatField(null=False,blank=False)
    pro_image=models.ImageField(upload_to=getfilename, height_field=None, width_field=None, max_length=None,null=True,blank=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False,help_text="0-default,1-hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-trending")
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            URL=self.pro_image.url
        except:
            URL=""
        return URL
        

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=True,blank=True)
    created_at=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.product.name 
    def get_total(self):
        return self.product_qty*self.product.new_price
    
class favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product
        
