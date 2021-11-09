from django.contrib import admin
from django.contrib.auth.models import Group
from base.models import Item, Category, Tag, Profile, Order
from django.contrib.auth import get_user_model
from base.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin


class TagInline(admin.TabularInline):
    model = Item.tags.through

class ItemAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags',]
    list_display = ['name', 'category', 'is_published']

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'username', 
                'email',
                'password',
            )
        }),
        (None, {
            'fields': (
                'is_active',
                'is_admin',
            )
        }),
    )
    list_display = ['username', 'email', 'is_active', 'is_admin']
    list_filter = []
    ordering = []
    filter_horizontal = []

    # 管理画面での新規作成時の項目
    add_fieldsets = (
        (None, {
            'fields': (
                'username', 
                'email',
                'is_active',
            )
        }),
    )
    
    add_form = UserCreationForm
    inlines = [ProfileInline]

admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(get_user_model(), CustomUserAdmin)

admin.site.unregister(Group)
