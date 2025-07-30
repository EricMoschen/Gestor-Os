from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import GroupAdmin

admin.site.unregister(Group)

class CustomGroupAdmin(GroupAdmin):
    filter_horizontal = ('permissions',)

admin.site.register(Group, CustomGroupAdmin)
admin.site.register(Permission)
