from django.contrib import admin
from .models import Event, Initiative, InitiativeGroup, InitiativeImage


class InitiativeImageInline(admin.TabularInline):
    model = InitiativeImage
    extra = 0


@admin.register(InitiativeGroup)
class InitiativeGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "display_order")
    list_filter = ("status",)
    search_fields = ("title", "lead")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ("title", "group", "category", "status", "display_order")
    list_filter = ("group", "category", "status")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (InitiativeImageInline,)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "timing", "event_date", "venue", "status")
    list_filter = ("timing", "status", "event_date")
    search_fields = ("title", "summary", "venue")
    prepopulated_fields = {"slug": ("title",)}
