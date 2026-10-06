from django.contrib import admin
from .models import PodcastEpisode, PodcastShow, Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "vertical", "publication_date", "status", "updated_at")
    list_filter = ("type", "vertical", "status", "publication_date")
    search_fields = ("title", "summary", "author")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-publication_date", "title")


@admin.register(PodcastShow)
class PodcastShowAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")


@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ("episode_number", "title", "published_date", "featured", "status")
    list_filter = ("status", "featured", "published_date")
    search_fields = ("title", "guest", "summary")
    prepopulated_fields = {"slug": ("title",)}
