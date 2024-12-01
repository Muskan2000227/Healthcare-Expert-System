from django.db import models
from ckeditor.fields import RichTextField
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
# Create your models here.
class contact_model(models.Model):
    name=RichTextField()
    email=models.EmailField()
    message=RichTextField()
    def __str__(self):
        return self.email


class register_model(models.Model):
    username=RichTextField()
    email=models.EmailField()
    passw=models.CharField(max_length=40)
    cpassw=models.CharField(max_length=40)
    phone_no=models.CharField(max_length=100,blank=True,null=True)
    Address=models.CharField(max_length=100,blank=True,null=True)
    pincode_no=models.CharField(max_length=10,blank=True,null=True)
    date_of_birth=models.CharField(max_length=20,blank=True,null=True)
    Bio=models.CharField(max_length=200,blank=True,null=True)
    image_ed=models.ImageField(upload_to="data",blank=True,null=True)
    

    def __str__(self):
        return self.email


class drug_model(models.Model):
    drug_name=models.CharField(max_length=200)
    uses_drug=RichTextField(blank=True,null=True )
    sideeffects_drug =RichTextField(blank=True,null=True)
    warning_drug=RichTextField(blank=True,null=True)
    precaution_drug=RichTextField(blank=True,null=True)
    interactions_Drug=RichTextField(blank=True,null=True)
    overdose_drug=RichTextField(blank=True,null=True)
    imgmain_Drug=RichTextField(blank=True,null=True)
    color_Drug=RichTextField(blank=True,null=True)
    shape_Drug=RichTextField(blank=True,null=True)
    imprint_Drug=RichTextField(blank=True,null=True)
    drug_title=RichTextField(blank=True,null=True)
    imags_drug=RichTextField(blank=True,null=True)
    genericname=models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.drug_name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    


class supplement_model(models.Model):
    supplement_name=models.CharField(max_length=200)
    overview_drug=RichTextField(blank=True,null=True )
    uses_drug=RichTextField(blank=True,null=True )
    sideeffects_drug =RichTextField(blank=True,null=True)
    precaution_drug=RichTextField(blank=True,null=True)
    interactions_Drug=RichTextField(blank=True,null=True)
    dosing_Drug=RichTextField(blank=True,null=True)
    othername=models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.supplement_name

    
class BodyPart(models.Model):
    name=models.CharField(max_length=200)

    

class Symptom(models.Model):
    name=models.CharField(max_length=200)
    body_part=models.ForeignKey(BodyPart,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Disease(models.Model):
    name=models.CharField(max_length=200)
    symptoms=models.ManyToManyField(Symptom)
    def __str__(self):
        return self.name

class Blogs(models.Model):
    title=RichTextField(blank=True,null=True )
    desc=RichTextField(blank=True,null=True )
    image=models.ImageField(upload_to='images/')
    bywho=RichTextField(blank=True,null=True )
    wdate=RichTextField(blank=True,null=True )
    def __str__(self):
        return self.title
    
class Pill(models.Model):
    imprint = models.CharField(max_length=100, help_text="Text or symbols imprinted on the pill")
    color = models.CharField(max_length=50, help_text="Color of the pill")
    shape = models.CharField(max_length=50, help_text="Shape of the pill")
    
    name = models.CharField(max_length=100, blank=True, null=True, help_text="Drug name")
    strength = models.CharField(max_length=50, blank=True, null=True, help_text="Strength of the pill")
    
    image_urls=models.ImageField(upload_to='images/')

   

    def __str__(self):
        return f"{self.name} - {self.imprint} ({self.color}, {self.shape})"    