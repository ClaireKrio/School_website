from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)

# Register your models here.
from accounts.models import CustomUser, Profile

for user in CustomUser.objects.all():
    profiles = Profile.objects.filter(user=user)
    if profiles.count() > 1:
        profiles[1:].delete()
