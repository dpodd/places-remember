from django.shortcuts import render
from django.http import HttpResponse

def index(request, *args, **kwargs):
    context = {}
    return render(request, 'index.html', context)