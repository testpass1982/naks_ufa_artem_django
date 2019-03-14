from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'mainapp/index.html')

def reestr(request):
    return render(request, 'mainapp/reestr.html')

def doc(request):
    return render(request, 'mainapp/doc.html')