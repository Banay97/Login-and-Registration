from django.db import models
import datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters long."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists."
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords should match."    
        if postData['DOB'] == "":
            errors['DOB'] = "Date of Birth is required."
        if postData['DOB'] > datetime.date.today().strftime("%Y-%m-%d"):
            errors['DOB'] = "Date of Birth should be in the past."
            
        return errors                    
        

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    DOB = models.DateField(max_length=8, blank=True, null=True)
    objects = UserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"