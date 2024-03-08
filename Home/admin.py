from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile,Quips

# Mix profile info into user info
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Quips)
