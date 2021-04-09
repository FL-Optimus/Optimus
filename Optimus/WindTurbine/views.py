from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import BladeForm
from .models import Blade

# Create your views here.
def home(request):
    return render(request, 'index.html')



# Create your views here.
def blade(request):
    blade = Blade.objects.all()
    print(blade)
    print('called')
    if request.method == "POST":
        print('POST')
        form = BladeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                print('SAVED')
                return redirect('/show')
            except:
                print('PASS')
                pass
    else:
        print('ELSE')
        form = BladeForm()
    return render(request,'index.html',{'form':form})


def show(request):
    blades = Blade.objects.all()
    return render(request,"components/blade/show.html",{'blades':blades})


def edit(request, id):
    blade = Blade.objects.get(id=id)
    return render(request,'components/blade/edit.html', {'blade':blade})


def update(request, id):
    instance = get_object_or_404(Blade, id=id)
    form = BladeForm(request.POST or None, instance=instance)
    print('FORM', form)
    if form.is_valid():
        form.save()
        print('IS VALID')
        return redirect("/show")
    print('NOT VALID')
    return render(request, 'components/blade/edit.html', {'blade': blade})


def destroy(request, id):
    blade = Blade.objects.get(id=id)
    blade.delete()
    return redirect("components/blade/show")


# if component == 'foundation':
# form = FoundationForm(request.POST or None)
# components = Foundation.objects.all()
# title = 'Foundation'

def detail_view(request, component):
    component = ContentType.objects.get(model='blade')
    blade = component.model_class()
    print(blade.__dict__)
    # try:
    #     component.objects.all()
    #     print('IT worked')
    # except:
    #     print('NOT WORKING')
    #     pass

    return HttpResponse('Component found')