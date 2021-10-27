from server.apps.accounts.models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = ('username', 'email', 'first_name', 'last_name', 'mobile', 'verification_code',
                    'is_superuser', 'is_staff', 'is_active', 'activation_token', )

    list_filter = ('username', 'first_name', 'last_name', 'user_created', 'is_superuser', 'is_staff', 'is_active', )

    ordering = ('user_created', 'username', 'first_name', 'is_superuser', 'is_staff', 'is_active', )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Main fields', {'fields': ('first_name', 'last_name', 'verification_code', 'user_created', )}
         ),
        ('Contacts', {'fields': ('email', 'mobile', )}
         ),
        ('Permissions', {'fields': ('groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')}
         ),
        )
    add_fieldsets = (
        ('Main fields', {
            'classes': ('wide', ),
            'fields': ('username', 'email', 'mobile', 'password1', 'password2', 'verification_code', )
            }),
        ('Permissions', {
            'classes': ('wide', ),
            'fields': ('groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')
        })
    )
    readonly_fields = ('user_created', )

    search_fields = ('username', 'first_name', 'last_name', 'mobile', 'email')
    filter_horizontal = ('groups', 'user_permissions',)
