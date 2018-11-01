from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or any(i.isdigit() for i in postData['first_name']):
            errors['first_name'] = "First name should be at least 2 characters with no numbers"
        if len(postData['last_name']) < 2 or any(i.isdigit() for i in postData['first_name']):
            errors['last_name'] = "Last name should be at least 2 characters with no numbers"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw'] :
            errors['password'] = "Passwords do not match"
        if len(postData['email']) < 1:
            errors['email'] = "Email field is empty"
        elif not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        print(user)
        # print(user[0])
        if len(postData['email']) < 1:
            errors['email'] = "Login email field is empty"
        elif not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address format"
        elif len(user) < 1:
            # try: 
            #     validate_email(postData['email'])
            # except:
            errors['email'] = "Email address is not registered"

        # user = User.objects.get(email=postData['email'])
        if len(postData['password']) < 8:
            errors['password'] = "Login password should be at least 8 characters"
        
        # elif not bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
        #     errors['password'] = "Login password is incorrect"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()