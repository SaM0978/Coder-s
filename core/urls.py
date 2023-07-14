from core import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),
    path('base', views.base, name="base"),
    path('items/<int:id>', views.items),
    path('payment/<int:id>', views.payment, name="payment"),
    path('signup', views.signup, name="signup"),
    path('login', views.logins, name="login"),
    path('logout', views.logouted, name="logout"),
]