from django.shortcuts import redirect, render, HttpResponse

def home(request):
    return render(request, 'index.html')