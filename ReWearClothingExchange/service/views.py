from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Login, UserDetails, Item
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from .form import UserDetailsForm 
from .item_form import ItemForm




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
        return redirect('login')
    
#     try:
#         user = Login.objects.get(email=email)
#     except Login.DoesNotExist:
#         return redirect('signup_login')
#     try:
#         details = UserDetails.objects.filter(user=user).first()
#   # get UserDetails linked to this user
#     except UserDetails.DoesNotExist:
#         details = None

#     items = user.items.all() if hasattr(user, 'items') else []

#     context = {
#         'user': user,
#         'details': details,
#         'items': items,
#     }  # or your login URL name
    return render(request, 'home.html', {'email': email})


def addItems(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('signup_login')

    try:
        user = Login.objects.get(email=user_email)
    except Login.DoesNotExist:
        return redirect('signup_login')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = user  # Link to logged-in user
            item.save()
            return redirect('dashboard')
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form, 'user_email': user_email})


def itemDetails(request, itemId):
    return HttpResponse(itemId)


def dashboard(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('signup_login')

    try:
        user = Login.objects.get(email=user_email)
    except Login.DoesNotExist:
        return redirect('signup_login')

    details = UserDetails.objects.filter(user=user).last()

    # ✅ Get only items created by this user
    items = Item.objects.filter(user=user)

    context = {
        'user': user,
        'details': details,
        'items': items,
    }
    return render(request, 'dashboard.html', context)


def add_user_info(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('signup_login')

    try:
        user = Login.objects.get(email=user_email)
    except Login.DoesNotExist:
        return redirect('signup_login')

    if request.method == 'POST':
        form = UserDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            details = form.save(commit=False)
            details.user = user
            details.save()
            return redirect('dashboard')
    else:
        form = UserDetailsForm()

    return render(request, 'add_user.html', {'form': form})


def logout(request):
    request.session.flush()  
    return redirect('signup_login')
