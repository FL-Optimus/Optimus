from django.shortcuts import render
from .models import Material
# Create your views here.
def home(request):
    return render(request, 'index.html')

def generator_list_view(request):
    types = [f'Type{i}' for i in range(1,5)]
    context = {
        'types': types
    }
    return render(request, 'components/generator/generator.html', context)

def generator_detail_view(request, gen_type):
    print(f'components/generator/types/{gen_type}.html')
    # types/{gen_type}

    return render(request, f'components/generator/types/{gen_type}.html')
