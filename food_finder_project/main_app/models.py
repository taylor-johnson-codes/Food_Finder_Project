from django.db import models
import re
import requests
from urllib.parse import urlencode, urlparse, parse_qsl
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
GOOGLE_API_KEY = "AIzaSyA_vt4l6ctQUT17lxgjvF2T_JRHTdb310I"

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
    # profile_pic = picture uploaded by user
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Upload(models.Model):
    file_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    image = models.ImageField(upload_to="profile_picture", default=None, blank=True, null=True)
    uploaded_by = models.ForeignKey(User, related_name="profile_pic", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Donator(models.Model):
    amount = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GoogleMapsClient(object):
    lat = None
    lng = None
    data_type = 'json'
    location_query = None
    api_key = None
    
    def __init__(self, api_key=None, address_or_postal_code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key == None:
            raise Exception ("API key is required")
        self.api_key = api_key
        self.location_query = address_or_postal_code
        if self.location_query != None:
            self.extract_lat_lng()
    
    def extract_lat_lng(self):
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        params = {"address": self.location_query, "key" : self.api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        if r.status_code not in range (200, 299):
            return {}
        latlng = {}
        try:
            latlng = r.json()['results'][0]['geometry']['location']
        except:
            pass
        lat,lng = latlng.get("lat"), latlng.get("lng")
        self.lat = lat
        self.lng = lng
        return lat, lng
    
    def search (self, keyword="food bank", radius=1000, location=None):
        lat, lng = self.lat, self.lng
        if location != None:
            lat, lng = self.extract_lat_lng(location=location)
        endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}"
        params = {
            "key" : self.api_key,
            "location" : f"{lat},{lng}",
            "radius" : radius,
            "keyword" : keyword
        }
        params_encoded = urlencode(params)
        places_url = f"{endpoint}?{params_encoded}"
        r = requests.get(places_url)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def detail(self, place_id="ChIJLfySpTOuEmsRsc_JfJtljdc"):
        detail_base_endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        detail_params = {
            "place_id" : f"{place_id}",
            "fields" : "name,formatted_address,formatted_phone_number,business_status",
            "key" : api_key
        }
        detail_params_encoded = urlencode(detail_params)
        detail_url = f"{detail_base_endpoint}?{detail_params_encoded}"
        r = requests.get(detail_url)
        if r.status_code not in range(200, 299):
            return {}

        return r.json()