from django.contrib import admin
from cart.models import Cart,Orderdetails,Payment
# Register your models here.
admin.site.register(Cart)
admin.site.register(Orderdetails)
admin.site.register(Payment)