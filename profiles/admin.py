from django.contrib import admin
from django.contrib.auth import get_user_model  # can also do from.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Profile

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    search_fields = ['email']
    list_display = ['email', 'is_active', 'is_staff', 'is_admin', 'last_login', 'timestamp']
    list_filter = ['is_active', 'is_staff',  'is_admin']
    ordering = ['email']
    filter_horizontal = []

    form = UserAdminChangeForm  # for updating user in admin
    add_form = UserAdminCreationForm    # for creating user in admin

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}), # if you have any personal info fields e.g. names, include them as strings in the empty tuple.
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')})
    )
    '''
    add_fieldsets is not a standard ModelAdmin attribute. UserAdmin overides get_fieldsets
    to use this attribute when creating a user. '''
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)

# if you are not using the groups, you can remove the Group model by:
admin.site.unregister(Group)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user']
    search_fields = ['first_name', 'last_name', 'user']