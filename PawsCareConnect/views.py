from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request , 'home.html')

def custom_404(request , exception):
    print('1111111111111111111111111111111')
    return render(request, '404.html' , {}, status=404)