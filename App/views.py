from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import RegisterForm
# Create your views here.


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('hahahhahahaha')
        else:
            return HttpResponse('??????')
    else:
        form = RegisterForm()
        context = {
            'form':form,
        }
        return render(request,'users/register.html',context)