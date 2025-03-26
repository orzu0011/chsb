from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, ViewPermissionRuleToUser, ViewPermissionRuleGroup, ViewPermissionRuleCategory, \
    ViewPermissionRule, ViewPermission, ViewPermissionRuleGroupToUser


# Inline admin classes for permissions
class ViewPermissionRuleToUserInline(admin.TabularInline):
    model = ViewPermissionRuleToUser
    min_num = 0
    extra = 0
    verbose_name = 'User Permission'
    verbose_name_plural = 'User Permissions'


class ViewPermissionRuleGroupToUserInline(admin.TabularInline):
    model = ViewPermissionRuleGroupToUser
    min_num = 0
    extra = 0
    verbose_name = 'User Permission Group'
    verbose_name_plural = 'User Permission Groups'


# Custom User admin for managing User and associated permissions
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'user_type', 'email', 'is_superuser', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'user_type')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ('user_permissions',)
    
    # Inline for permissions associated with the user
    inlines = [ViewPermissionRuleToUserInline, ViewPermissionRuleGroupToUserInline]

    # Fields displayed in the user creation/edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'avatar', 'email', 'user_type', 'birthday', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    # Additional user-specific fields for the admin form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'birthday', 'phone', 'user_type', 'is_active', 'is_staff')
        }),
    )

    # Modify the default ordering of the User model
    ordering = ('username',)


# Admin registrations for other models related to permissions and roles

@admin.register(ViewPermission)
class ViewPermissionAdmin(admin.ModelAdmin):
    list_display = ('view_name', 'path_name', 'method')
    search_fields = ('view_name', 'path_name')
    list_filter = ('method',)


@admin.register(ViewPermissionRule)
class ViewPermissionRuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'permission', 'category', 'position')
    search_fields = ('title',)
    list_filter = ('category',)


@admin.register(ViewPermissionRuleCategory)
class ViewPermissionRuleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'position')
    search_fields = ('title',)
    list_filter = ('position',)


@admin.register(ViewPermissionRuleGroup)
class ViewPermissionRuleGroupAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('permissions',)
    search_fields = ('title',)


@admin.register(ViewPermissionRuleToUser)
class ViewPermissionRuleToUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission',)
    search_fields = ('user__username',)
    list_filter = ('permission',)


@admin.register(ViewPermissionRuleGroupToUser)
class ViewPermissionRuleGroupToUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'group',)
    search_fields = ('user__username',)
    list_filter = ('group',)


