from django.db import models
from apps.core.models import PublishableModel


class InitiativeGroup(PublishableModel):
    slug = models.SlugField(unique=True)
    eyebrow = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    lead = models.TextField(blank=True)
    intro = models.TextField(blank=True)
    image = models.ImageField(upload_to="initiatives/groups/", blank=True)
    link_to_events = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")

    def __str__(self):
        return self.title


class Initiative(PublishableModel):
    group = models.ForeignKey(InitiativeGroup, related_name="initiatives", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=280)
    tag = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    eyebrow = models.CharField(max_length=100, blank=True)
    lead = models.TextField(blank=True)
    overview = models.JSONField(default=list, blank=True)
    impact = models.JSONField(default=list, blank=True)
    date_label = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=180, blank=True)
    category = models.CharField(max_length=120, blank=True)
    participants = models.CharField(max_length=100, blank=True)
    initiative_status = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="initiatives/covers/", blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")

    def __str__(self):
        return self.title


class InitiativeImage(models.Model):
    initiative = models.ForeignKey(Initiative, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="initiatives/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "id")


class Event(PublishableModel):
    class Timing(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        PAST = "past", "Past"

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=280)
    timing = models.CharField(max_length=10, choices=Timing.choices, db_index=True)
    registration_status = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    event_date = models.DateField(null=True, blank=True, db_index=True)
    display_date = models.CharField(max_length=120, blank=True)
    event_time = models.CharField(max_length=100, blank=True)
    venue = models.CharField(max_length=180, blank=True)
    format = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="events/", blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("event_date", "display_order", "title")

    def __str__(self):
        return self.title
