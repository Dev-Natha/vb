from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("login/", loginView, name="login"),
    path("register/", registration, name="register"),
    path("logout/", logoutView, name="logout"),
    path("get-placed-bets/", get_placed_bets, name="get-placed-bets"),
    path("placurstak/", stake, name="stake"),
    path("deletestake/", deleteStake, name="deletestake"),
    path("profile/", profile, name="profile"),
    path("payment/", payment, name="payment"),
]
