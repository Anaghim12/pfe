from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User ,Type
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','email','first_name','last_name','type','is_active'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','is_active','type')
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['role']
    def __str__(self):
        return self.type