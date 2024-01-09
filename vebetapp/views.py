from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

# Create your views here.
@csrf_exempt
def home(request):
    profileform = ProfileForm()
    total_stakes = []
    total_odds = []
    bet_model = BetModel.objects.all()
    if request.user.is_authenticated:
        placed_bet = PlacedBet.objects.filter(user=request.user)
        profile = Profile.objects.get(user=request.user)
        profileform = ProfileForm(instance=profile)
    else:
        placed_bet = []

    if request.method == 'POST':
        data_from_frontend = request.POST.get('input_data', '')
        for bet in placed_bet:
            total_stakes.append(bet.odds * int(data_from_frontend))
            total_odds.append(bet.odds)
            
        return JsonResponse({"result":sum(total_stakes), "total_odds":sum(total_odds)})
    else:
        total_bet = 0

    context = {"bet_model":bet_model, "placed_bet":placed_bet, "total_bet":total_bet, "profileform":profileform}
    return render(request, "index.html", context)

def registration(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = MyRegisterationForm()
    if request.method == "POST":
        form = MyRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("home")
    context = {"form":form}
    return render(request, "register.html", context)

def loginView(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid Login Details")
            return redirect("login")
    return render(request, "login.html")

def logoutView(request):
    logout(request)
    return redirect("home")

@csrf_exempt
def stake(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            stake_id = request.POST.get('stake_id', '')
            stake_value = request.POST.get('stake_value', '')
            stake_name = request.POST.get('stake_name', '')
            bet_model = BetModel.objects.get(id=stake_id)
            placed_bet = PlacedBet.objects.filter(user=request.user, bet_model=bet_model, name=stake_name, odds=stake_value)
            if placed_bet:
                placed_bet.delete()
            else:
                new_bet = PlacedBet.objects.create(user=request.user, bet_model=bet_model, name=stake_name, odds=stake_value, team1_name=bet_model.team1_name, team2_name=bet_model.team2_name)
                new_bet.save()
            return JsonResponse({"result":"okay"})
        else:
            return JsonResponse({"result": "Authentication required"})

@csrf_exempt
def get_placed_bets(request):
    if request.user.is_authenticated:
        all_bets = list(PlacedBet.objects.filter(user=request.user).values())
        return JsonResponse({"result": all_bets})
    else:
        return JsonResponse({"output": "You are not logged in yet"})

@csrf_exempt
def deleteStake(request):
    if request.method == "POST":
        element_id = request.POST.get('element_id', '')
        placed_bet = PlacedBet.objects.get(id = element_id)
        placed_bet.delete()
        return JsonResponse({"result":"Success"})

@login_required(login_url="login")
def profile(request):
    profile = Profile.objects.get(user=request.user)
    profileform = ProfileForm(instance=profile)
    userform = MyRegisterationForm(instance=request.user)
    if request.method == "POST":
        profileform = ProfileForm(request.POST, request.FILES, instance=profile)
        if profileform.is_valid():
            id_form = profileform.save(commit=False)
            id_form.user = request.user
            id_form.save()
            return redirect("profile")
        else:
            print("not done")
    context = {"profile":profile, "profileform":profileform, "userform":userform}
    return render(request, "dashboard.html", context)

def payment(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        paymentform = request.FILES.get("paymentfile")
        if paymentform:
            profile.payment = paymentform
            profile.save()
            placed_bet = PlacedBet.objects.filter(user=request.user)
            placed_bet.delete()

    return redirect("home")