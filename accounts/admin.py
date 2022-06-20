from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm,CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('favorite_musics','favorite_instrument')
    add_form = CustomUserCreationForm
    form  = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets +(
        (None,{'fields' : ('favorite_musics','favorite_instrument')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('favorite_musics','favorite_instrument')}),
    )
admin.site.register(CustomUser,CustomUserAdmin)