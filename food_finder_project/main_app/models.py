from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager): 
    def validate_registration(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name needs to be at least 2 characters."
        elif postData['first_name'].isalpha() == False:
            errors['first_name_alpha'] = "First name needs to be letters only."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name needs to be at least 2 characters."
        elif postData['last_name'].isalpha() == False:
            errors['last_name_alpha'] = "Last name needs to be letters only."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format."
        elif User.objects.filter(email = postData['email']):
            errors['email_exists'] = "Email already exists in database."
        if len(postData['phone']) < 10:
            errors['phone'] = "Phone number needs to be at least 10 numbers."
        elif postData['phone'].isdigit() == False:
            errors['phone_digit'] = "Phone number can only consist of numbers."
        if len(postData['zipcode']) < 5:
            errors['city'] = "Zip code needs to be at least 5 characters."
        if len(postData['password']) < 8:
            errors['password'] = "Password needs to be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm'] = "Password and confirm password don't match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    zipcode = models.IntegerField()
    password = models.CharField(max_length=100)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)