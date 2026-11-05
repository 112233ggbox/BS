from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Department, User

@admin.register(User)
class EnterpriseUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("企业信息", {"fields": ("full_name", "department", "confirmed")}),)

admin.site.register(Department)
