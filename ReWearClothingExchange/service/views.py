from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Login


def combined_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'signup':
            email = request.POST.get('email')
            password = request.POST.get('pass')
            c_password = request.POST.get('c_pass')

            if password != c_password:
                messages.error(request, "Passwords do not match.")
            elif Login.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                Login.objects.create(email=email, password=password, c_password=c_password)
                messages.success(request, "Account created successfully!")

        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('pass')

            try:
                user = Login.objects.get(email=email, password=password)
                request.session['user_email'] = user.email  # Save user session
                messages.success(request, f"Welcome back, {user.email}!")
                return redirect('home')  # Make sure 'home' URL exists
            except Login.DoesNotExist:
                messages.error(request, "Invalid login credentials.")

    return render(request, 'auth/signup_login.html')


def home(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login')  # or your login URL name
    return render(request, 'home.html', {'email': email})


def items(request):
    return HttpResponse("This is Home page")

def itemDetails(request, itemId):
    return HttpResponse(itemId)


def dashboard(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('auth/signup_login.html')  # Redirect if not logged in

    try:
        user = Login.objects.get(email=user_email)
    except Login.DoesNotExist:
        return redirect('auth/signup_login.html')

    user_items = user.items.all()  # all items uploaded by user

    context = {
        'user': user,
        'items': user_items,
    }
    return render(request, 'dashboard.html', context)