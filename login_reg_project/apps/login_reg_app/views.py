from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from .models import *
import bcrypt

def index(request):
    print('INDEX method')
    return render(request, 'login_reg_app/index.html')

# def register(request):
#     print('REGISTER method')
#     user = User.objects.create(
#         first_name = request.POST['first_name'],
#         last_name = request.POST['last_name'],
#         email = request.POST['email'],
#         password = request.POST['password']
#     )
#     request.session['first_name'] = request.POST['first_name']

#     print('REGISTER works!!')
#     return redirect('/success')

def register(request):
    print('REGISTER method')
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        print('IF REGISTER')
        for key, value in errors.items():
            messages.error(request, value)
        print('IF WORKS!!')
        return redirect('/')
    else: 
        hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hashpw)
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashpw
        )
        request.session['first_name'] = request.POST['first_name']
    print('ELSE works!!')
    return redirect('/success')

def login(request):
    print('LOGIN method')
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        print('FAILED LOGIN')
        for key, value in errors.items():
            messages.error(request, value)
        print('FAILED ELSE WORKS!!')
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("password match")

        return redirect('/success')

# def login(request):
#     print('LOGIN method')
#     user = User.objects.get(email=request.POST['email'])
#     if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
#         print("password match")

#         return redirect('/success')
#     else:
#         print("failed password")
#         messages.add_message(request, messages.INFO, 'Invalid password')
#         return redirect('/')
    

def success(request):
    print('SUCCESS method')

    print('SUCCESS WORKS!')
    return render(request, 'wall_app/wall.html')
