from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# Create your models here.
class BetModel(models.Model):
    home = models.DecimalField(decimal_places=2, max_digits=10)
    draw = models.DecimalField(decimal_places=2, max_digits=10)
    away = models.DecimalField(decimal_places=2, max_digits=10)
    team1_name = models.CharField(max_length=200)
    team2_name = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    score1 = models.IntegerField()
    score2 = models.IntegerField()

    def __str__(self):
        return self.team1_name + " vs " + self.team2_name

class PlacedBet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet_model = models.ForeignKey(BetModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    odds = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    team1_name = models.CharField(max_length=200, null=True)
    team2_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.bet_model.team1_name + " vs " + self.bet_model.team2_name + " " + self.name

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=200, blank=True, null=True)
    account_number = models.CharField(max_length=200, blank=True, null=True)
    wallet_address = models.CharField(max_length=200, blank=True, null=True)
    wallet_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username   

class Profile(models.Model):
    profile_id = models.UUIDField(default=uuid.uuid4, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserProfile", blank=True)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, blank=True)
    profile_picture = models.ImageField(upload_to="profilepic", default="profile.jpg")
    payment = models.ImageField(upload_to="paymentpic", null=True, blank=True)

    def __str__(self):
        return self.user.username  
