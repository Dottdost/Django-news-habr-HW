from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_banned', 'is_staff', 'ban_unban_button', 'make_admin_button')
    list_filter = ('role', 'is_banned', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('More', {'fields': ('role', 'is_banned')}),
    )

    actions = ['make_admin', 'make_user', 'ban_user', 'unban_user']

    def ban_unban_button(self, obj):
        if obj.is_banned:
            return format_html(f'<a class="button" href="/admin/accounts/user/{obj.id}/unban/">Unban</a>')
        else:
            return format_html(f'<a class="button" href="/admin/accounts/user/{obj.id}/ban/">Ban</a>')
    ban_unban_button.short_description = 'Бан'

    def make_admin_button(self, obj):
        if obj.role == 'ADMIN':
            return format_html(f'<a class="button" href="/admin/accounts/user/{obj.id}/make_user/">Make admin</a>')
        elif obj.role == 'USER':
            return format_html(f'<a class="button" href="/admin/accounts/user/{obj.id}/make_admin/">= Make admin</a>')
        return '-'
    make_admin_button.short_description = 'Admin'

    @admin.action(description="Make admin")
    def make_admin(self, request, queryset):
        queryset.update(role='ADMIN')

    @admin.action(description="Make user")
    def make_user(self, request, queryset):
        queryset.update(role='USER')

    @admin.action(description="Ban")
    def ban_user(self, request, queryset):
        queryset.update(is_banned=True)

    @admin.action(description="Unban")
    def unban_user(self, request, queryset):
        queryset.update(is_banned=False)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/ban/', self.admin_site.admin_view(self.ban_user_action), name='ban_user'),
            path('<int:user_id>/unban/', self.admin_site.admin_view(self.unban_user_action), name='unban_user'),
            path('<int:user_id>/make_admin/', self.admin_site.admin_view(self.make_admin_action), name='make_admin'),
            path('<int:user_id>/make_user/', self.admin_site.admin_view(self.make_user_action), name='make_user'),
        ]
        return custom_urls + urls

    def ban_user_action(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.is_banned = True
        user.save()
        self.message_user(request, f"user {user.username} baned.")
        from django.shortcuts import redirect
        return redirect(request.META.get('HTTP_REFERER', '/admin/accounts/user/'))

    def unban_user_action(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.is_banned = False
        user.save()
        self.message_user(request, f"User {user.username} unban.")
        from django.shortcuts import redirect
        return redirect(request.META.get('HTTP_REFERER', '/admin/accounts/user/'))

    def make_admin_action(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.role = 'ADMIN'
        user.save()
        self.message_user(request, f"User {user.username} now is admin.")
        from django.shortcuts import redirect
        return redirect(request.META.get('HTTP_REFERER', '/admin/accounts/user/'))

    def make_user_action(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.role = 'USER'
        user.save()
        self.message_user(request, f"User {user.username} not admin anymore.")
        from django.shortcuts import redirect
        return redirect(request.META.get('HTTP_REFERER', '/admin/accounts/user/'))
