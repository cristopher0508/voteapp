from django.contrib import admin
from .models import UserProfile, User, voteImages, Notification
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(voteImages)
admin.site.register(Notification)

