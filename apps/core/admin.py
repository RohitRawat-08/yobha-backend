from django.contrib import admin
from .models import HomepageMetric, Milestone, Partner, SiteSettings, Testimonial, Value


class PublishedAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("name", "title")
    ordering = ("display_order",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (("Identity", {"fields": ("name", "short_name", "abbreviation", "tagline", "description", "established")}),("Contact", {"fields": ("address", "phone", "email", "office_hours", "map_embed_url", "social_links")}))


@admin.register(Testimonial)
class TestimonialAdmin(PublishedAdmin):
    list_display = ("name", "role", "status", "display_order", "updated_at")
    search_fields = ("name", "role", "quote")


@admin.register(HomepageMetric, Partner, Value, Milestone)
class OrderedContentAdmin(PublishedAdmin):
    list_display = ("__str__", "status", "display_order", "updated_at")
