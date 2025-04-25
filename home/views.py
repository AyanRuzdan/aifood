from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
def home_view(request):
    return render(request, 'home/home.html')
@login_required
def dashboard(request):
    user = request.user
    return render(request, 'dashboard/dashboard.html', {'user': user})