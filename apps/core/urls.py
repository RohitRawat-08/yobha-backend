from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api import (
    BillBriefViewSet, BookViewSet, EventViewSet, HomepageMetricViewSet,
    InitiativeGroupViewSet, InitiativeViewSet, IssueBriefViewSet, MilestoneViewSet,
    PartnerViewSet, PersonCategoryViewSet, PersonViewSet, PodcastEpisodeViewSet,
    PodcastShowViewSet, PublicationViewSet, ReportViewSet, SiteSettingsViewSet,
    TestimonialViewSet, ValueViewSet,
)

router = DefaultRouter()
router.register("publications", PublicationViewSet, basename="publication")
router.register("issue-briefs", IssueBriefViewSet, basename="issue-brief")
router.register("bill-briefs", BillBriefViewSet, basename="bill-brief")
router.register("books", BookViewSet, basename="book")
router.register("reports", ReportViewSet, basename="report")
router.register("initiative-groups", InitiativeGroupViewSet, basename="initiative-group")
router.register("initiatives", InitiativeViewSet, basename="initiative")
router.register("events", EventViewSet, basename="event")
router.register("podcast", PodcastShowViewSet, basename="podcast")
router.register("podcast-episodes", PodcastEpisodeViewSet, basename="podcast-episode")
router.register("people", PersonViewSet, basename="person")
router.register("people-categories", PersonCategoryViewSet, basename="people-category")
router.register("testimonials", TestimonialViewSet, basename="testimonial")
router.register("homepage-metrics", HomepageMetricViewSet, basename="homepage-metric")
router.register("partners", PartnerViewSet, basename="partner")
router.register("values", ValueViewSet, basename="value")
router.register("milestones", MilestoneViewSet, basename="milestone")
router.register("site-settings", SiteSettingsViewSet, basename="site-settings")

urlpatterns = [path("", include(router.urls))]
