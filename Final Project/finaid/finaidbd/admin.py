from django.contrib import admin
from .models import User, Deal_officer, Order, Installment

# Register your models here.
admin.site.register(User)
admin.site.register(Deal_officer)
admin.site.register(Order)
admin.site.register(Installment)
