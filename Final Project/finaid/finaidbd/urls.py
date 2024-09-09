from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("installment/<int:id>", views.installment, name="installment"),
    path("order", views.order, name="order"),
    path("pending_order", views.pnd_ordr, name="pnd_ordr"),
    path("pending_installment", views.pnd_inst, name="pnd_inst"),
    path("paid_products", views.paid, name="paid"),
    path("dealers", views.dealers, name="dealers"),
    path("pay_inst", views.pay_inst, name="pay_inst"),
]
