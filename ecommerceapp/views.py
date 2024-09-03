from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse
from .models import storetype,items,itemsdetails,cart
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login ,authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm,LoginUserForm
# Create your views here.

def index(request):

    template=loader.get_template('index.html')
    return HttpResponse(template.render({'request':request}))

def basket(request):

    template=loader.get_template('basket.html')
    return HttpResponse(template.render({'request':request}))

def listitems(request):
     p=items.objects.filter(st_id=2)
     template=loader.get_template('listitems.html')
     return HttpResponse(template.render({'items':p,'request':request}))

def perlistitems(request):
     p=items.objects.filter(st_id=5)
     template=loader.get_template('perlistitems.html')
     return HttpResponse(template.render({'items':p,'request':request}))


def detials(request,id):
      template=loader.get_template('details.html')
      data=itemsdetails.objects.select_related('items').filter(items_id=id).first()
      data.total=data.qty*data.items.price
      return HttpResponse(template.render({'data':data,'request':request}))

@login_required(login_url='/auth_login/')
def checkout(request):
      template=loader.get_template('checkout.html')
      return HttpResponse(template.render({'request':request}))

@csrf_exempt
def add_to_cart(request):
     id=request.POST.get("id")
     p=cart(itmesid=id)
     p.save()
     row=cart.objects.all()
     count=0
     for item in row:
          count=count+1   
     request.session["cart"]=count
     return JsonResponse({'count':count})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

def auth_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('checkout')  # Assuming 'checkout' is the name of your URL pattern
            else:
                return HttpResponse("Invalid login.")
        else:
            return HttpResponse("Invalid form data.")
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'auth_login.html', context)




def auth_register(request):
     pass
     
     



    