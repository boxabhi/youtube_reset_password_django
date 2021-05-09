from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login,logout
from .helpers import send_forget_password_mail

def Login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if not username or not password:
                messages.success(request, 'Both Username and Password are required.')
                return redirect('/login/')
            user_obj = User.objects.filter(username = username).first()
            if user_obj is None:
                messages.success(request, 'User not found.')
                return redirect('/login/')
        
        
            user = authenticate(username = username , password = password)
            
            if user is None:
                messages.success(request, 'Wrong password.')
                return redirect('/login/')
        
            login(request , user)
            return redirect('/')

                
            
            
    except Exception as e:
        print(e)
    return render(request , 'login.html')



def Register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register/')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register/')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
    
            profile_obj = Profile.objects.create(user = user_obj )
            profile_obj.save()
            return redirect('/login/')

        except Exception as e:
            print(e)

    except Exception as e:
            print(e)

    return render(request , 'register.html')


def Logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def Home(request):
    return render(request , 'home.html')



def ChangePassword(request , token):
    context = {}
    
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')
            
            
            
        
        
    except Exception as e:
        print(e)
    return render(request , 'change-password.html' , context)


import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'forget-password.html')