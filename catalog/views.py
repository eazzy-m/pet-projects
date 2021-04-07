from django.shortcuts import render

# Create your views here. yes   war


def main(request):
    return render(request, 'main.html')