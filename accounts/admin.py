from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Account

class AccountAdmin(UserAdmin):
    list_display = ['full_name', 'email', 'username', 'last_login', 'date_joined', 'is_active']
    list_display_links = ('email', 'full_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()   # the below three lines are used alter the password field into read only format
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)