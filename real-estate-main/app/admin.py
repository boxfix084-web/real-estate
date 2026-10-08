from django.contrib import admin

from .models import Property, SavedProperty


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'property_type',
        'purpose',
        'city',
        'price',
        'owner',
        'is_featured',
        'created_at'
    )

    list_filter = (
        'property_type',
        'purpose',
        'city',
        'is_featured'
    )

    search_fields = (
        'title',
        'location',
        'city'
    )


@admin.register(SavedProperty)
class SavedPropertyAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'property',
        'created_at'
    )