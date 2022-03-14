from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User ,Type
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','email','first_name','last_name'),
        }),
    )

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['role']