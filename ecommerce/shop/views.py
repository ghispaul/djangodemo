from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth import authenticate, login,logout


from django.contrib.auth.models import User



from django.http import HttpResponse
# Create your views here.
def allcategories(request):
    c=Category.objects.all()
    context={'cat':c}
    return render(request,'category.html',context)

def allproducts(request,p):
    c=Category.objects.get(id=p)
    k=Product.objects.filter(category=c)
    context = {'cat':c, 'pro':k}
    return render(request,'products.html',context)

def details(request,a):
    c=Product.objects.get(id=a)
    context={'details':c}
    return render(request, 'details.html', context)


def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']

        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:categories')
        else:
            return HttpResponse("invalid")

    return render(request,'login.html')

def register(request):
    if (request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        cp= request.POST['cp']
        f= request.POST['f']
        l= request.POST['l']
        e= request.POST['e']

        if(p==cp):
            u=User.objects.create_user(username=u,password=p,first_name=f,last_name=l,email=e)
            u.save()
        else:
            return HttpResponse("password is not same")
        return redirect('shop:login')

    return render(request,'register.html')
def user_logout(request):
    logout(request)
    return redirect('shop:login')


def addcategory(request):
    if(request.method=='POST'):
        n=request.POST['n']
        i=request.FILES['i']
        d=request.POST['d']

        c=Category.objects.create(name=n,image=i,desc=d)
        c.save()
        return redirect('shop:categories')

    return render(request,'addcategory.html')

def addproduct(request):
    if(request.method=='POST'):
        n=request.POST['n']
        i=request.FILES['i']
        d=request.POST['d']
        s=request.POST['s']
        p=request.POST['p']
        c=request.POST['c']
        cat=Category.objects.get(name=c)

        p=Product.objects.create(name=n,image=i,desc=d,stock=s,price=p,category=cat)
        p.save()
        return redirect('shop:categories')
    return render(request,'addproduct.html')


def addstock(request,h):
    p=Product.objects.get(id=h)
    if(request.method=="POST"):
        p.stock=request.POST['n']
        p.save()
        return redirect('shop:categories')
    context={'pro':p}
    return render(request,'addstock.html',context)