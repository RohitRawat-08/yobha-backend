from django.db import models
from apps.core.models import PublishableModel


class PersonCategory(PublishableModel):
    slug = models.SlugField(unique=True)
    kind = models.CharField(max_length=20, choices=(("people", "People"), ("profile", "Profile")), default="people")
    eyebrow = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    lead = models.TextField(blank=True)
    intro = models.TextField(blank=True)
    image = models.ImageField(upload_to="people/categories/", blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "title")

    def __str__(self):
        return self.title


class Person(PublishableModel):
    category = models.ForeignKey(PersonCategory, related_name="people", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=180)
    designation = models.CharField(max_length=180, blank=True)
    bio = models.TextField(blank=True)
    short_bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="people/", blank=True)
    email = models.EmailField(blank=True)
    social_links = models.JSONField(default=list, blank=True)
    additional_details = models.JSONField(default=dict, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")

    def __str__(self):
        return self.name
