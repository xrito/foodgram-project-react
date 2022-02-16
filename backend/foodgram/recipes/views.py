from django.shortcuts import render

def index(request):
    return render(request, '.frontend/static/frontend/index.html')

