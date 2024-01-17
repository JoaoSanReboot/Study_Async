from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages

def cadastro(request):

    if request.method == "GET":
         return render(request, 'cadastro.html')
    elif request.method == "POST":
         username = request.POST.get('username')
         senha = request.POST.get('senha')
         confirmar_senha = request.POST.get('confirmar_senha')

         if not senha == confirmar_senha:
              messages.add_message(request, constants.ERROR, 'Senha e confirmar senha não coincidem')
              return redirect('/usuarios/cadastro')
         
         user = User.objects.filter(username=username)

         if user.exists():
              messages.add_message(request, constants.ERROR, 'Usuario já existe')
              return redirect('/usuarios/cadastro')
         
         try:    
               User.objects.create_user(
                    username=username,
                    password=senha
               )
               return redirect('/usuarios/login')#error
         except:
              messages.add_message(request, constants.ERROR, 'Error interno do servidor')
              return redirect('/usuarios/cadastro')