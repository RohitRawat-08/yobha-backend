from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class PublishableModel(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    name = models.CharField(max_length=180, default="Youth of Bharat Foundation")
    short_name = models.CharField(max_length=120, blank=True)
    abbreviation = models.CharField(max_length=30, blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    established = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    office_hours = models.CharField(max_length=120, blank=True)
    map_embed_url = models.URLField(blank=True)
    social_links = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Testimonial(PublishableModel):
    quote = models.TextField()
    name = models.CharField(max_length=160)
    role = models.CharField(max_length=180, blank=True)
    image = models.ImageField(upload_to="testimonials/", blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")

    def __str__(self):
        return self.name


class HomepageMetric(PublishableModel):
    value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=20, blank=True)
    label = models.CharField(max_length=160)
    detail = models.CharField(max_length=160, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order",)


class Partner(PublishableModel):
    name = models.CharField(max_length=180, unique=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")


class Value(PublishableModel):
    title = models.CharField(max_length=180)
    description = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order",)


class Milestone(PublishableModel):
    year = models.CharField(max_length=20)
    title = models.CharField(max_length=180)
    description = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order",)
