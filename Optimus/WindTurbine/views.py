from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def generator_list_view(request):
    types = [f'Type{i}' for i in range(1,5)]
    context = {
        'types': types
    }
    return render(request, 'generator.html', context)