from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BetModel)
admin.site.register(PlacedBet)
admin.site.register(AdminProfile)
admin.site.register(Profile)