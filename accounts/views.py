from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import UserProfile
from django.contrib.auth import login, logout
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def create_shipment(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.user = request.user
            food_item.save()

            return redirect('sender_dashboard')
    else:
        form = FoodItemForm()
    return render(request, 'monitoring/create_shipment.html', {'form': form})