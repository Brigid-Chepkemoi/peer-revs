from django.contrib import admin
from .models import UserProfile,Projects,Category,Rating

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Projects)
admin.site.register(Category)
admin.site.register(Rating)