
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Bíblia 3D', {'fields': ('tipo',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Bíblia 3D', {'fields': ('tipo',)}),
    )
