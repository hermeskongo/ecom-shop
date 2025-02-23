from django.contrib import admin

# Register your models here.
from accounts.models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'address', 'date_joined', 'last_login', 'is_active')
    
    list_display_links = ('first_name', 'last_name')
    list_editable = ('is_active',)
    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country')


