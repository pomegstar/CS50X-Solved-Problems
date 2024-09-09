from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Deal_officer(models.Model):
    name = models.CharField(max_length=64)
    mobile = models.IntegerField()
    pic = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"Deal_officer: {self.name}"

class Order(models.Model):
    #orderer's fields
    product = models.CharField(max_length=1000)
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orderer")
    referenced_by = models.ForeignKey(Deal_officer, on_delete=models.CASCADE, related_name="refer")
    time = models.DateTimeField(auto_now_add=True)
    maxim_price = models.IntegerField()
    monthly_pay = models.IntegerField()

    #admin's fields
    is_accept = models.BooleanField(default=False)
    final_price = models.IntegerField(blank=True, null=True)
    mnthpay_final = models.IntegerField(blank=True, null=True)
    due = models.IntegerField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ordered_by.username} orders {self.product}."

class Installment(models.Model):
    orderer = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders")
    paid = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    #admins's field
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.orderer.ordered_by.username} paid {self.paid} tk"
