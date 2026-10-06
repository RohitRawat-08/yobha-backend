from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.content.models import PodcastEpisode, PodcastShow, Publication
from apps.initiatives.models import Event, Initiative, InitiativeGroup
from apps.people.models import Person, PersonCategory
from .models import HomepageMetric, Milestone, Partner, SiteSettings, Testimonial, Value


class PublicReadAdminWrite(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(request.user and request.user.is_staff)


class PublishedViewSet(viewsets.ModelViewSet):
    permission_classes = (PublicReadAdminWrite,)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(status="published")


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class InitiativeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initiative
        fields = ("slug", "title", "tag", "description", "image")


class InitiativeSerializer(serializers.ModelSerializer):
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = Initiative
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def get_gallery(self, instance):
        return [{"image": image.image.url, "caption": image.caption} for image in instance.gallery.all()]


class InitiativeGroupSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = InitiativeGroup
        fields = ("id", "slug", "eyebrow", "title", "lead", "intro", "image", "link_to_events", "display_order", "status", "items")

    def get_items(self, instance):
        queryset = instance.initiatives.all()
        if not self.context["request"].user.is_staff:
            queryset = queryset.filter(status="published")
        return InitiativeCardSerializer(queryset, many=True, context=self.context).data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class PodcastEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastEpisode
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class PodcastShowSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()

    class Meta:
        model = PodcastShow
        fields = ("eyebrow", "title", "lead", "intro", "platforms", "cover_image", "episodes")

    def get_episodes(self, instance):
        queryset = PodcastEpisode.objects.all()
        if not self.context["request"].user.is_staff:
            queryset = queryset.filter(status="published")
        return PodcastEpisodeSerializer(queryset, many=True, context=self.context).data


class PersonSerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    class Meta:
        model = Person
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class PersonCategorySerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = PersonCategory
        fields = ("id", "slug", "kind", "eyebrow", "title", "lead", "intro", "image", "display_order", "status", "members")

    def get_members(self, instance):
        queryset = instance.people.all()
        if not self.context["request"].user.is_staff:
            queryset = queryset.filter(status="published")
        return PersonSerializer(queryset, many=True, context=self.context).data


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"


class HomepageMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageMetric
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = "__all__"


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = "__all__"


class PublicationViewSet(PublishedViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        content_type = self.request.query_params.get("type") or getattr(self, "publication_type", None)
        vertical = self.request.query_params.get("vertical")
        search = self.request.query_params.get("search")
        if content_type:
            queryset = queryset.filter(type=content_type)
        if vertical:
            queryset = queryset.filter(vertical__iexact=vertical)
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(summary__icontains=search) | queryset.filter(author__icontains=search)
        return queryset.distinct()


class IssueBriefViewSet(PublicationViewSet):
    publication_type = Publication.Type.ISSUE_BRIEF


class BillBriefViewSet(PublicationViewSet):
    publication_type = Publication.Type.BILL_BRIEF


class BookViewSet(PublicationViewSet):
    publication_type = Publication.Type.BOOK


class ReportViewSet(PublicationViewSet):
    publication_type = Publication.Type.REPORT


class InitiativeGroupViewSet(PublishedViewSet):
    queryset = InitiativeGroup.objects.prefetch_related("initiatives").all()
    serializer_class = InitiativeGroupSerializer
    lookup_field = "slug"


class InitiativeViewSet(PublishedViewSet):
    queryset = Initiative.objects.select_related("group").prefetch_related("gallery").all()
    serializer_class = InitiativeSerializer
    lookup_field = "slug"


class EventViewSet(PublishedViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        timing = self.request.query_params.get("timing")
        return queryset.filter(timing=timing) if timing else queryset


class PodcastShowViewSet(viewsets.ViewSet):
    permission_classes = (PublicReadAdminWrite,)

    def list(self, request):
        show = PodcastShow.objects.first()
        if show is None:
            return Response({}, status=404)
        return Response(PodcastShowSerializer(show, context={"request": request}).data)


class PodcastEpisodeViewSet(PublishedViewSet):
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer
    lookup_field = "slug"


class PersonViewSet(PublishedViewSet):
    queryset = Person.objects.select_related("category").all()
    serializer_class = PersonSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        return queryset.filter(category__slug=category) if category else queryset


class PersonCategoryViewSet(PublishedViewSet):
    queryset = PersonCategory.objects.prefetch_related("people").all()
    serializer_class = PersonCategorySerializer
    lookup_field = "slug"


class TestimonialViewSet(PublishedViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class HomepageMetricViewSet(PublishedViewSet):
    queryset = HomepageMetric.objects.all()
    serializer_class = HomepageMetricSerializer


class PartnerViewSet(PublishedViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class ValueViewSet(PublishedViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer


class MilestoneViewSet(PublishedViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer


class SiteSettingsViewSet(viewsets.ViewSet):
    permission_classes = (PublicReadAdminWrite,)

    def list(self, request):
        settings = SiteSettings.objects.first()
        if settings is None:
            return Response({}, status=404)
        return Response(SiteSettingsSerializer(settings).data)
