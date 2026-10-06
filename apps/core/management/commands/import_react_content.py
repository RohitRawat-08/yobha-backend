import json
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.content.models import PodcastEpisode, PodcastShow, Publication
from apps.core.models import HomepageMetric, Milestone, Partner, SiteSettings, Testimonial, Value
from apps.initiatives.models import Event, Initiative, InitiativeGroup, InitiativeImage
from apps.people.models import Person, PersonCategory


TYPE_MAP = {
    "Article": "article", "Issue Brief": "issue_brief", "Bill Brief": "bill_brief",
    "Book": "book", "Report": "report",
}


class Command(BaseCommand):
    help = "Imports the JSON exported from the existing React data modules."

    def add_arguments(self, parser):
        parser.add_argument("--source", default=str(settings.BASE_DIR / "import_data" / "react-content.json"))

    def handle(self, *args, **options):
        source = Path(options["source"])
        if not source.exists():
            raise CommandError(f"Export source not found: {source}. Run `node scripts/export-react-content.mjs` first.")
        data = json.loads(source.read_text(encoding="utf-8"))
        self.project_root = settings.BASE_DIR.parent
        self.import_publications(data["publications"])
        self.import_initiatives(data["initiatives"])
        self.import_events(data["upcomingEvents"], "upcoming")
        self.import_events(data["pastEvents"], "past")
        self.import_podcast(data["podcast"], data["episodes"])
        self.import_people(data["directory"])
        self.import_core(data)
        self.stdout.write(self.style.SUCCESS("React content imported successfully."))

    def copy_media(self, source_ref):
        if not source_ref or not isinstance(source_ref, str) or not source_ref.startswith("/src/"):
            return ""
        relative = Path(unquote(source_ref.lstrip("/")))
        original = self.project_root / relative
        if not original.exists():
            self.stderr.write(f"Missing source asset: {original}")
            return ""
        target = settings.MEDIA_ROOT / "imported" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(original, target)
        return str(target.relative_to(settings.MEDIA_ROOT)).replace("\\", "/")

    @staticmethod
    def parse_date(value):
        if not value:
            return None
        for date_format in ("%Y-%m-%d", "%d %B %Y"):
            try:
                return datetime.strptime(value, date_format).date()
            except ValueError:
                continue
        return None

    def import_publications(self, records):
        for record in records:
            publication, _ = Publication.objects.update_or_create(
                slug=record["id"],
                defaults={
                    "title": record["title"], "type": TYPE_MAP[record["type"]],
                    "vertical": record.get("vertical", ""), "summary": record.get("summary", ""),
                    "author": record.get("author", ""), "display_date": record.get("displayDate", ""),
                    "cover_image": self.copy_media(record.get("image")),
                    "document": self.copy_media(record.get("file")), "document_type": record.get("fileType", ""),
                    "status": "published",
                },
            )

    def import_initiatives(self, groups):
        for group_slug, group in groups.items():
            group_obj, _ = InitiativeGroup.objects.update_or_create(
                slug=group_slug,
                defaults={
                    "eyebrow": group.get("eyebrow", ""), "title": group.get("title", group_slug.title()),
                    "lead": group.get("lead", ""), "intro": group.get("intro", ""),
                    "image": self.copy_media(group.get("image")), "link_to_events": group.get("linkToEvents", False),
                    "status": "published",
                },
            )
            for index, record in enumerate(group.get("items", [])):
                details = record.get("details", {})
                initiative, _ = Initiative.objects.update_or_create(
                    slug=record["slug"],
                    defaults={
                        "group": group_obj, "title": record.get("title", ""), "tag": record.get("tag", ""),
                        "description": record.get("description", ""), "eyebrow": details.get("eyebrow", ""),
                        "lead": details.get("lead", ""), "overview": details.get("overview", []),
                        "impact": details.get("impact", []), "date_label": details.get("date", ""),
                        "location": details.get("location", ""), "category": details.get("category", ""),
                        "participants": details.get("participants", ""), "initiative_status": details.get("status", ""),
                        "image": self.copy_media(record.get("image")), "display_order": index, "status": "published",
                    },
                )
                InitiativeImage.objects.filter(initiative=initiative).delete()
                for image_index, image in enumerate(details.get("gallery", [])):
                    copied = self.copy_media(image)
                    if copied:
                        InitiativeImage.objects.create(initiative=initiative, image=copied, display_order=image_index)

    def import_events(self, records, timing):
        for index, record in enumerate(records):
            Event.objects.update_or_create(
                slug=record["id"],
                defaults={
                    "title": record["title"], "timing": timing, "registration_status": record.get("status", ""),
                    "summary": record.get("description", record.get("summary", "")),
                    "event_date": self.parse_date(record.get("date")), "display_date": record.get("displayDate", ""),
                    "event_time": record.get("time", ""), "venue": record.get("venue", ""),
                    "format": record.get("format", ""), "image": self.copy_media(record.get("image")),
                    "display_order": index, "status": "published",
                },
            )

    def import_podcast(self, podcast, episodes):
        PodcastShow.objects.update_or_create(
            pk=1,
            defaults={"eyebrow": podcast.get("eyebrow", "Podcast"), "title": podcast["title"], "lead": podcast.get("lead", ""),
                      "intro": podcast.get("intro", ""), "platforms": podcast.get("platforms", []),
                      "cover_image": self.copy_media(podcast.get("cover"))},
        )
        for index, record in enumerate(episodes):
            number = int(record["number"])
            PodcastEpisode.objects.update_or_create(
                slug=record["id"],
                defaults={"episode_number": number, "title": record["title"], "guest": record.get("guest", ""),
                          "summary": record.get("summary", ""), "duration": record.get("duration", ""),
                          "published_date": self.parse_date(record.get("date")), "display_date": record.get("date", ""),
                          "thumbnail": self.copy_media(record.get("image")), "featured": record.get("featured", index == 0),
                          "status": "published"},
            )

    def import_people(self, directory):
        for index, (slug, entry) in enumerate(directory.items()):
            if entry.get("kind") not in {"people", "profile"}:
                continue
            category, _ = PersonCategory.objects.update_or_create(
                slug=slug,
                defaults={"kind": entry["kind"], "eyebrow": entry.get("eyebrow", ""), "title": entry.get("title", ""),
                          "lead": entry.get("lead", ""), "intro": entry.get("intro", ""),
                          "image": self.copy_media(entry.get("image")), "display_order": index, "status": "published"},
            )
            records = entry.get("members", entry.get("profiles", []))
            for person_index, record in enumerate(records):
                person_slug = f"{slug}-{person_index + 1}"
                Person.objects.update_or_create(
                    slug=person_slug,
                    defaults={"category": category, "name": record.get("name", ""),
                              "designation": record.get("role", record.get("designation", "")),
                              "bio": record.get("bio", record.get("description", "")),
                              "short_bio": record.get("shortBio", ""), "image": self.copy_media(record.get("image")),
                              "additional_details": record, "display_order": person_index, "status": "published"},
                )

    def import_core(self, data):
        site = data["site"]
        contact = data["contact"]
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={"name": site["name"], "short_name": site.get("shortName", ""), "abbreviation": site.get("abbr", ""),
                      "tagline": site.get("tagline", ""), "description": site.get("description", ""),
                      "established": site.get("established", ""),
                      "address": "\n".join(contact.get("addressLines") or [contact.get("address", "")]),
                      "phone": contact.get("phone", ""), "email": contact.get("email", ""),
                      "office_hours": contact.get("hours", ""), "map_embed_url": contact.get("mapEmbed", ""),
                      "social_links": data.get("socials", [])},
        )
        self.replace_ordered(Testimonial, data["testimonials"], lambda item, index: {"quote": item["quote"], "name": item["name"], "role": item.get("role", ""), "display_order": index, "status": "published"})
        self.replace_ordered(HomepageMetric, data["heroMetrics"], lambda item, index: {"value": item["value"], "suffix": item.get("suffix", ""), "label": item["label"], "display_order": index, "status": "published"})
        self.replace_ordered(Partner, data["partners"], lambda item, index: {"name": item, "display_order": index, "status": "published"})
        self.replace_ordered(Value, data["values"], lambda item, index: {"title": item["title"], "description": item["description"], "display_order": index, "status": "published"})
        self.replace_ordered(Milestone, data["milestones"], lambda item, index: {"year": item["year"], "title": item["title"], "description": item["description"], "display_order": index, "status": "published"})

    @staticmethod
    def replace_ordered(model, records, mapper):
        model.objects.all().delete()
        model.objects.bulk_create([model(**mapper(record, index)) for index, record in enumerate(records)])
