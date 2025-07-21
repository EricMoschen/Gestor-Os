from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import auth

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            return redirect('/menuos/')
        
        messages.add_message(request, constants.ERROR, 'Username ou senha inválidos.')
        return redirect('login')
    
