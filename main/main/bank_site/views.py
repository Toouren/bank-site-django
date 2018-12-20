from django.shortcuts import render


def return_index(request):
    return render(request, 'main_templates/login.html')


def return_login_index(request):
    return render(request, 'registration/login.html')

# Create your views here.
