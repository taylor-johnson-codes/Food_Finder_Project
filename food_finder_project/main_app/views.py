from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import uuid
import stripe
stripe.api_key = "sk_test_51HAqUDDoKNbVzjhL68N7W2SW5fqholag7JTD8q89HrImiHmomRlFQfYnHPTGPl7gNC8pHVtbq1hLmuI9H3ZjUlSX00v3BF6FXG"

# need to pip install pillow
# need to pip install stripe

def index(request):
    return render(request, 'index.html')

def volunteer(request):
    return render(request, 'volunteer.html')

def registration(request):
    return render(request, 'registration.html')

def register(request):
    errors = User.objects.validate_registration(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/registration')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        zipcode = request.POST['zipcode']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, zipcode=zipcode, password=pw_hash)
        request.session['user_id'] = new_user.id
        return redirect('/profile')

def login(request):
    return render(request, 'login.html')

def process_login(request):
    email = request.POST['email']
    password = request.POST['password']
    user_list = User.objects.filter(email=email)
    if len(user_list) > 0:
        logged_user = user_list[0]
        if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/profile')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('/login')
    else:
        messages.error(request, "Email doesn't exist in the database. Try again or sign up.")
        return redirect('/login')

def profile(request):
    if not "user_id" in request.session:
        messages.error(request, "You must be logged in to see your profile.")
        return redirect('/login')
    else:
        user = User.objects.get(id=request.session['user_id'])
        all_upload = Upload.objects.all()
        # check user.profile.len if 0 use dummy. if >0 use
        if len(user.profile_pic.all()) == 0:
            pictures = user.profile_pic.all()
        else:
            pictures = user.profile_pic.all()[0]
        context = {
            'user': user,
            'picture' : pictures,
            'all_upload' : all_upload,
        }
        return render(request, 'profile.html', context)

def change_picture(request):
    this_user = User.objects.get(id=request.session['user_id'])
    old_pic = Upload.objects.filter(uploaded_by=this_user)
    old_pic.delete()
    file_name = request.FILES["upload_image"].name
    request.FILES["upload_image"].name = "{}.{}".format(uuid.uuid4().hex, file_name.split(".")[-1])
    image = request.FILES["upload_image"]
    uploaded_by = User.objects.get(id=request.session['user_id'])
    Upload.objects.create(file_name=file_name, image=image, uploaded_by=uploaded_by)
    return redirect("/profile")

def edit_profile(request):
    user = User.objects.get(id=request.session['user_id'])
        # check user.profile.len if 0 use dummy. if >0 use
    if len(user.profile_pic.all()) == 0:
        pictures = user.profile_pic.all()
    else:
        pictures = user.profile_pic.all()[0]
    context = {
        'user': user,
        'picture' : pictures,
    }
    return render(request, 'edit_profile.html', context)

def update_profile(request):
    errors = User.objects.validate_registration(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_profile')
    else:
        user_id = request.POST['user_id']
        user = User.objects.get(id=user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.zipcode = request.POST['zipcode']
        user.password = request.POST['password']
        pw_hash = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
        user.save()
        return redirect('/profile')

def delete(request):
    user_id = request.POST['user_id']
    user = User.objects.get(id=user_id)
    user.delete()
    request.session.clear()
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def search(request):
    return render(request, 'search.html')

def zipsearch(request):
    return render(request, 'zipsearch.html')

def donate(request):
    return render(request, 'donate_testpage.html')
    
def donate2(request):
    return render(request, 'donate_testpage2.html')

def charge(request):
    # amount = float(request.POST['amount'])
    amount = "${:,.2f}".format(float(request.POST['amount']))
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    new_donator = Donator.objects.create(amount=amount, first_name=first_name, last_name=last_name, email=email)
    donator_id = new_donator.id
    return redirect('/thank_you/' + str(donator_id))

def thank_you(request, donator_id):
    donator = Donator.objects.get(id=donator_id)
    context = {
        'donator' : donator
    }
    return render(request, 'thank_you.html', context)

def delete_db(request):
    all_donators = Donator.objects.all()
    all_donators.delete()
    return redirect('/')
    return render(request, 'donate.html')

def backup(request):
    return render(request, 'back_up.html')
