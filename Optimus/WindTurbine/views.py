from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def generator_list_view(request):
    return render(request, 'generator.html')