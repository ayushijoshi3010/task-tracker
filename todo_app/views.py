from django.shortcuts import render,redirect,get_object_or_404
from todo_app.models import TODOO
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def signup_view(request):
    if request.method=='POST':
        data=request.POST
        username=data.get('fname')
        email=data.get('email')
        password=data.get('pwd')
        if User.objects.filter(username=username).exists():
            messages.error(request,"User already exists")
        else:

            my_user=User.objects.create_user(username,email,password)
            my_user.save()
            messages.success(request,"Account created Successfully")
            print(f"Username is {username} \n Email is {email} \n Password is {password}")
            return redirect('login_view')
        
       
    return render(request,'signup.html')

def login_view(request):
    if request.method=='POST':
        data=request.POST
        username=data.get('fname')
        password=data.get('pwd')
        user=authenticate(request,username=username,password=password)
# Internally authenticate kregi user model s match kregi ki milta julta user stored h User model m ya nahi
        if user is not None:
            login(request,user) # login krwa do user ko
            print(f"Username is {username} \nPassword is {password}")
            return redirect('todo_view')
        else:
            messages.error(request,"Invalid Credentials")
            

        

    return render(request,'login.html')

@login_required
def todo_view(request):
    if request.method=='POST':
        data=request.POST
        title=data.get('title')
        print(title)
        obj=TODOO(title=title,user=request.user)
        obj.save()
    res=TODOO.objects.filter(user=request.user).order_by('-date')
   
    return render(request,'todo.html',{'res':res})


def todo_edit(request,pk):
    obj=get_object_or_404(
        TODOO,
        srno=pk,
        user=request.user
    )
    if request.method=='POST':
        data=request.POST
        title=data.get('title')
        obj.title=title
        obj.save()
        return redirect('todo_view')
    return render(request,'todo_edit.html',{'title':obj})

def todo_delete(request,pk):
    obj=get_object_or_404(
        TODOO,
        srno=pk,
        user=request.user
    )
    if request.method=='POST':
        obj.delete()
        return redirect('todo_view')
    return render(request,'todo_delete.html',{'todo':obj})

def logout_view(request):
    logout(request)
    return redirect('login_view')