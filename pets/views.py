from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import requests, json, googlemaps, petfinder, datetime

from .forms import UserForm
gmaps = googlemaps.Client(key = 'AIzaSyDWRoV2ae3J-BCp0LKXcoFdmpHxIEQnXXE')
petapi = petfinder.PetFinderClient(api_key='b41019e06145925caa78884c95a3f60e', api_secret='0a2d8f1549b50a91fb47bb707f3663d2')

# Create your views here.

def toCleanedTime(str):
    return ' '.join(str.split('T'))

class Home(View):
    def get(self, request):
        if request.user.is_authenticated():
            return render(request, 'pets/index.html')
        form = UserForm()
        return render(request, 'pets/index.html', {'form':form})

def Log_out(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')

def About(request):
    return render(request, 'pets/main.html')

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
    lost_json = requests.get(lost_url).json()
    map(lambda x: x.__setitem__('date',datetime.datetime.strptime(x['date'][:10],'%Y-%m-%d')), lost_json)

    context = {
        'adopt' : lost_json
    }
    return render(request, 'pets/adopt.html', context)

def Lost(request):
    lost_url = 'https://data.kingcounty.gov/resource/murn-chih.json'
    lost_json = requests.get(lost_url).json()
    map(lambda x: x.__setitem__('date',datetime.datetime.strptime(x['date'][:10],'%Y-%m-%d')), lost_json)

    context = {
    'lost' : lost_json,
    }
    return render(request, 'pets/lost.html', context)

def Found(request):
    lost_url = 'https://data.kingcounty.gov/resource/murn-chih.json'
    lost_json= requests.get(lost_url).json()
    map(lambda x: x.__setitem__('date',datetime.datetime.strptime(x['date'][:10],'%Y-%m-%d')), lost_json)

    context = {
    'found' : lost_json,
    }
    return render(request, 'pets/found.html', context)
