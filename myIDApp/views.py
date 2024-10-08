from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control

from django.contrib import messages


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request,'home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registerPage(request):
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.success(request,"Password does not follow the rules")
    context={'form':form}

    return render(request, 'register.html', context)

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginPage(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return redirect('home')
    else:
        print(request.method)
        if request.method=="POST":
            username=request.POST.get("username")
            password=request.POST.get("password")
            print(username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request,"Username or Password is incorrect")
        context={}
        print("H")
        return render(request,'login.html',context)
    

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutPage(request):
    logout(request)
    return redirect('login')

