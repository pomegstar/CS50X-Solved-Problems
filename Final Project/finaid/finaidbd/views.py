from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, Deal_officer, Order, Installment

def index(request):
    if request.user.is_authenticated:
        d = Order.objects.filter(is_accept=True, is_complete=False).order_by('time').reverse()
        p_ordr = Order.objects.filter(is_complete=False, ordered_by=request.user).order_by('time').reverse()
        return render(request, "finaidbd/index.html", {
         "orders": d,
         "p_orders": p_ordr,
         "heading": "Active",
         "heading_gu": "Orders"
        })
    else:
        return render(request, "finaidbd/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "finaidbd/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "finaidbd/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "finaidbd/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "finaidbd/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "finaidbd/register.html")

@login_required
def installment(request, id):
    ordr = Order.objects.get(pk=id)
    inst = Installment.objects.filter(orderer=ordr).order_by('datetime').reverse()
    if request.method == "POST":
        amnt = request.POST["inst_pay"]
        instlmnt = Installment(
            orderer = ordr,
            paid = amnt,
        )
        instlmnt.save()
        return render(request, "finaidbd/installment.html", {
            "installments": inst,
            "order": ordr,
            "mssage": "Installment paid successfully! Wait for admin confirmation."
        })

    else:
        return render(request, "finaidbd/installment.html", {
            "installments": inst,
            "order": ordr
        })

@login_required
def order(request):
    dealer = Deal_officer.objects.all()
    if request.method == "POST":
        prdct = request.POST["product"]
        delr = Deal_officer.objects.get(pk=request.POST["dealer"])
        inst = request.POST["installment"]
        mxm = request.POST["maximum"]
        ord = Order(
            product = prdct,
            ordered_by = request.user,
            referenced_by = delr,
            monthly_pay = inst,
            maxim_price = mxm,
        )
        ord.save()
        return render(request, "finaidbd/order.html", {
            "dealers": dealer,
            "mssage": "Your order is submitted succesfully! Wait for admin confirmation."
        })
    else:
        return render(request, "finaidbd/order.html", {
            "dealers": dealer
        })

@login_required
def pnd_ordr(request):
    pndor = Order.objects.filter(is_accept=False).order_by('time').reverse()
    if request.method == "POST":
       id = request.POST["prdr_id"]
       fprice = request.POST["fprice"]
       finst  = request.POST["finst"]
       prdr = Order.objects.get(pk=id)
       prdr.is_accept = True
       prdr.final_price = fprice
       prdr.mnthpay_final = finst
       prdr.due = fprice
       prdr.save()
       return redirect('pnd_ordr')
    else:
        return render(request, "finaidbd/pnd_ordr.html", {
            "p_orders":pndor
        })

@login_required
def pnd_inst(request):
    inst = Installment.objects.filter(is_accepted=False).order_by('datetime').reverse() #reverse order
    if request.method == "POST":
       id = request.POST["prdr_id"]
       prdr = Installment.objects.get(pk=id)
       prdr.is_accepted = True
       prdr.orderer.due -= prdr.paid
       if prdr.orderer.due == 0:
           prdr.orderer.is_complete = True
       prdr.save()
       prdr.orderer.save()
       if request.POST["pend_i"] == "True":
            return redirect('pnd_inst')
       else:
           return redirect('installment', id=prdr.orderer.id)
    else:
        return render(request, "finaidbd/pnd_inst.html", {
            "p_insts":inst
        })

@login_required
def paid(request):
        d = Order.objects.filter(is_accept=True, is_complete=True).order_by('time').reverse()
        p_ordr = Order.objects.filter(is_accept=True, is_complete=True, ordered_by=request.user).order_by('time').reverse()
        return render(request, "finaidbd/index.html", {
         "orders": d,
         "p_orders": p_ordr,
         "heading": "Completed",
         "heading_gu": "Completed Orders"
        })

@login_required
def dealers(request):
    delr = Deal_officer.objects.all()
    return render(request, 'finaidbd/dealers.html', {
        "dealers": delr
    })

@login_required
def pay_inst(request):
    ordrs = Order.objects.filter(is_accept=True, is_complete=False, ordered_by=request.user)
    if request.method == "POST":
        ord = Order.objects.get(pk=request.POST["ordr_no"])
        inst_paid = request.POST["installment"]

        instlmnt = Installment(
            orderer = ord,
            paid = inst_paid,
        )
        instlmnt.save()
        return render(request, "finaidbd/pay_inst.html", {
            "orders": ordrs,
            "mssage": "Installment paid successfully! Wait for admin confirmation."
        })

    else:
        return render(request, 'finaidbd/pay_inst.html', {
            "orders": ordrs
        })
