from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models
from apps.core.models import PublishableModel


def validate_upload_size(file):
    if file.size > 25 * 1024 * 1024:
        raise ValidationError("Uploads must be 25 MB or smaller.")


class Publication(PublishableModel):
    class Type(models.TextChoices):
        ARTICLE = "article", "Article"
        ISSUE_BRIEF = "issue_brief", "Issue Brief"
        BILL_BRIEF = "bill_brief", "Bill Brief"
        BOOK = "book", "Book"
        REPORT = "report", "Report"

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=320)
    type = models.CharField(max_length=20, choices=Type.choices, db_index=True)
    vertical = models.CharField(max_length=120, blank=True, db_index=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=180, blank=True)
    publication_date = models.DateField(null=True, blank=True, db_index=True)
    display_date = models.CharField(max_length=100, blank=True)
    cover_image = models.ImageField(upload_to="publications/covers/", blank=True)
    document = models.FileField(upload_to="publications/documents/", blank=True, validators=[FileExtensionValidator(["pdf", "ppt", "pptx", "doc", "docx"]), validate_upload_size])
    document_type = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ("-publication_date", "title")

    def __str__(self):
        return self.title


class PodcastShow(models.Model):
    eyebrow = models.CharField(max_length=80, default="Podcast")
    title = models.CharField(max_length=200)
    lead = models.TextField(blank=True)
    intro = models.TextField(blank=True)
    platforms = models.JSONField(default=list, blank=True)
    cover_image = models.ImageField(upload_to="podcasts/covers/", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PodcastEpisode(PublishableModel):
    slug = models.SlugField(unique=True)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=280)
    guest = models.CharField(max_length=180, blank=True)
    summary = models.TextField(blank=True)
    duration = models.CharField(max_length=40, blank=True)
    published_date = models.DateField(null=True, blank=True, db_index=True)
    display_date = models.CharField(max_length=100, blank=True)
    thumbnail = models.ImageField(upload_to="podcasts/episodes/", blank=True)
    audio_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ("-published_date", "-episode_number")

    def __str__(self):
        return f"Episode {self.episode_number}: {self.title}"
