from django.contrib import admin
from .models import Person, PersonCategory


@admin.register(PersonCategory)
class PersonCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "status", "display_order")
    list_filter = ("kind", "status")
    search_fields = ("title", "lead")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "category", "status", "display_order")
    list_filter = ("category", "status")
    search_fields = ("name", "designation", "bio")
    prepopulated_fields = {"slug": ("name",)}
