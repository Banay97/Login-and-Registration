from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

# Create your views here.
def index(request):
    user = User.objects.all()
    return render(request, 'login_and_registration.html', {'user': user})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Find the user by email
        user = User.objects.filter(email=email).first()
        
        # Check if the user exists and the password is correct
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['email'] = email
            messages.success(request, 'Welcome!')
            return render(request, 'success.html', {'user': user})

        else:
            messages.error(request, 'Invalid email or password', extra_tags='login')
            return redirect('index')
    return redirect('index')
        

def register(request):
    if request.method == 'POST':
        errors = User.objects.validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('index')
        else:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            user.save()
            
            messages.success(request, 'Registration successful! Please log in.')
            return render(request, 'success.html', {'user': user})
    return redirect('index')


def logout(request):
    if request.method == 'POST':
        request.session.clear()
        messages.success(request, 'Logout successful!', extra_tags='logout')
        return redirect('index')
    return redirect('index')




    