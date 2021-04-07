from django.shortcuts import render

# Create your views here. yes   w


def main(request):
    return render(request, 'main.html')