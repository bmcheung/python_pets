from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import requests, json, googlemaps

from .forms import UserForm
gmaps = googlemaps.Client(key = 'AIzaSyDWRoV2ae3J-BCp0LKXcoFdmpHxIEQnXXE')

# Create your views here.

class Home(View):
    def get(self, request):
        if request.user.is_authenticated():
            return render(request, 'pets/index.html')
        form = UserForm()
        return render(request, 'pets/index.html', {'form':form})
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(username = data['username'], password = data['password'])
                if user is not None:
                    login(request, user)
                    return redirect(reverse('pets:home'))
            except:
                messages.add_message(request, messages.ERROR, 'Username must be unique.')
        return redirect(reverse('pets:home'))

class Register(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect(request,'pets/index.html')
        form = UserForm()
        return render(request, 'pets/register.html', {'form':form})
    def post(self, request):
        form = UserForm(request.POST)
        form_type = request.POST['extra']
        if form.is_valid():
            data = form.cleaned_data
            if form_type == '0':
                try:
                    user = User.objects.create_user(username = data['username'], password = data['password'])
                    if user is not None:
                        login(request, user)
                        return redirect(reverse('pets:home'))
                except:
                    messages.add_message(request, messages.ERROR, 'Username must be unique.')
            elif form_type == '1':
                user = authenticate(username=data['username'], password=data['password'])
                if user is not None:
                    login(request, user)
                    return redirect(reverse('pets:home'))
                else:
                    messages.add_message(request, messages.ERROR, 'Username or password is incorrect')
        return redirect(reverse('pets:register'))

def Map(request):
    buy_url = 'https://data.kingcounty.gov/resource/nu2t-d4hv.json'
    buy_json = requests.get(buy_url).json()
    lost_url = 'https://data.kingcounty.gov/resource/murn-chih.json'
    lost_json= requests.get(lost_url).json()

    context = {
        'store' : buy_json,
        'lost' : lost_json
    }
    return render(request, 'pets/map.html', context)

def Adopt(request):
    lost_url = 'https://data.kingcounty.gov/resource/murn-chih.json'
    lost_json= requests.get(lost_url).json()
    context = {
        'adopt' : lost_json
    }
    return render(request, 'pets/adopt.html', context)

def Lost(request):
    lost_url = 'https://data.kingcounty.gov/resource/murn-chih.json'
    lost_json= requests.get(lost_url).json()
    context = {
    'lost' : lost_json,
    }
    return render(request, 'pets/lost.html', context)
def Lost_process(request):
    if request.method == 'POST':
        Pet.objects.create(
            name = request.POST['name'],
            breed = request.POST['breed'],
            location_lost = request.POST['location_lost'],
            date_lost = request.POST['date_lost'],
            status = 'LOST',
            notes = request.POST['notes'],
            image = request.POST['image'],
            listed_by = User.objects.get(id = request.session['id'])
        )
    return redirect(reverse('login:lost'))
def Found(request):
    lost_url = 'https://data.kingcounty.gov/resource/murn-chih.json'
    lost_json= requests.get(lost_url).json()
    context = {
    'found' : lost_json,
    }
    return render(request, 'pets/found.html', context)
def found_process(request):
    if request.method == 'POST':
        Pet.objects.create(
            name = request.POST['name'],
            breed = request.POST['breed'],
            location_lost = request.POST['location_lost'],
            date_lost = request.POST['date_lost'],
            status = 'FOUND',
            notes = request.POST['notes'],
            image = request.POST['image'],
            listed_by = User.objects.get(id = request.session['id'])
        )
    return redirect(reverse('login:found'))
