from django.contrib import admin

from accounts.models import Code, Profile, CustomUser, RoleChoice

admin.site.register(Code)
admin.site.register(Profile)
admin.site.register(CustomUser)
# Register your models here.
