from django.test import TestCase

from apps.content.models import Publication
from apps.initiatives.models import Event


class PublicApiTests(TestCase):
    def setUp(self):
        Publication.objects.create(
            title="Published article",
            slug="published-article",
            type=Publication.Type.ARTICLE,
            status="published",
        )
        Publication.objects.create(
            title="Draft article",
            slug="draft-article",
            type=Publication.Type.ARTICLE,
            status="draft",
        )
        Event.objects.create(
            title="Published event",
            slug="published-event",
            timing="upcoming",
            status="published",
        )

    def test_publication_list_hides_drafts(self):
        response = self.client.get("/api/v1/publications/")

        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        self.assertEqual([item["slug"] for item in results], ["published-article"])

    def test_type_alias_filters_publications(self):
        response = self.client.get("/api/v1/issue-briefs/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)

    def test_event_timing_filter(self):
        response = self.client.get("/api/v1/events/?timing=upcoming")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
