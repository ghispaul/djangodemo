from django.shortcuts import render


# Create your views here.
from shop.models import Product

from django.db.models import Q


def search_items(request):
    query = ''
    p = None

    if(request.method=="POST"):

        query = request.POST.get('q')

        if(query):

            p=Product.objects.filter(Q(name__icontains=query))


    return render(request,'search.html',{'pro':p,'k':query})

