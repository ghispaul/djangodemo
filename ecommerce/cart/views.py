from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart,Payment,Orderdetails
from shop.models import Product
from django.contrib.auth.models import User
import razorpay
from django.contrib.auth import login
@login_required
def add_to_cart(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        c=Cart.objects.get(user=u,product=p)
        if(p.stock>0):

            c.quantity+=1
            c.save()
            p.stock-=1
            p.save()
    except:
        if(p.stock>0):

            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()
            p.stock-=1
            p.save()


    return redirect('cart:cartview')

def cart_view(request):
    u=request.user
    c=Cart.objects.filter(user=u)
    total=0
    for i in c:
        total+=i.quantity*i.product.price

    context={'cart':c,'total':total}
    return render(request,'cart.html',context)
@login_required
def cart_remove(request,s):
    p=Product.objects.get(id=s)
    u=request.user

    try:
        c=Cart.objects.get(user=u,product=p)
        if(c.quantity>1):
            c.quantity-=1
            c.save()
            p.stock+=1
            p.save()
        else:
            c.delete()
            p.stock += 1
            p.save()

    except:
        pass

    return redirect('cart:cartview')


def delete_cart(request,t):
    u=request.user
    p=Product.objects.get(id=t)
    c=Cart.objects.get(user=u,product=p)
    if(c.quantity>0):
        p.stock += c.quantity
        c.delete()
        p.save()
        return redirect('cart:cartview')

@login_required
def orderform(request):
    if(request.method=="POST"):
        address=request.POST['address']
        phone=request.POST['phone']
        pin=request.POST['pin']

        u=request.user

        c=Cart.objects.filter(user=u)

        total=0

        for i in c:
            total+=i.quantity*i.product.price
        total=int(total*100)
        print(total)

        client=razorpay.Client(auth=('rzp_test_m0oGroJJDxngbH','cQV6PHLCKLoa0NzwQTkN23kl'))

        response_payment=client.order.create(dict(amount=total,currency="INR"))
        # print(response_payment)
        order_id=response_payment['id'] #retrive order id from response
        order_status=response_payment['status'] #retrive order statu from response
        if(order_status=='created'):
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Orderdetails.objects.create(product=i.product,user=u,no_of_items=i.quantity,address=address,phone=phone,pin=pin,order_id=order_id)
                o.save()
        else:
            pass
        response_payment['name']=u.username
        context={'payment':response_payment}

        return render(request,'payment.html',context)

    return render(request,'order.html')


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def payment_status(request, u):
    user = User.objects.get(username=u)
    if(not request.user.is_authenticated):
        login(request,user)
    if(request.method=="POST"):
        response=request.POST
        print(response)
        print(u)
        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }

        client = razorpay.Client(auth=('rzp_test_m0oGroJJDxngbH', 'cQV6PHLCKLoa0NzwQTkN23kl')) #to create a razorpay client


        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)

            p=Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id=response['razorpay_payment_id'] #adds the payment id after successful payment
            p.paid=True
            p.save()



            o=Orderdetails.objects.filter(user=user,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status='paid'
                i.save()



            c=Cart.objects.filter(user=user)
            print(c)
            c.delete()

        except:
            pass
    return render(request,'payment_status.html',{'status':True})

@login_required
def order_view(request):
    u=request.user
    o=Orderdetails.objects.filter(user=u,payment_status='paid')
    context={'orders':o,}
    return render(request,'order_view.html',context)