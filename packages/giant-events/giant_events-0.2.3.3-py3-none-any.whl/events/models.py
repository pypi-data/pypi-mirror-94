from django.db import models
from django.urls import reverse

from cms.models import PlaceholderField
from filer.fields.image import FilerImageField
from django.db.models.functions import Now

from mixins.models import (
    PublishingMixin,
    PublishingQuerySetMixin,
    TimestampMixin,
    URLMixin,
)


class Tag(TimestampMixin):
    """
    Model to store a tag for the Event model
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        """
        String representation of a Tag object, in the Events app
        """
        return self.name


class Location(TimestampMixin):
    """
    Location that is tied to an event
    """

    name = models.CharField(max_length=255, unique=True)
    lng = models.DecimalField(max_digits=12, decimal_places=10)
    lat = models.DecimalField(max_digits=12, decimal_places=10)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ["name"]

    def __str__(self):
        """
        String representation of the location object, in the Events app
        """
        return self.name


class EventQuerySet(PublishingQuerySetMixin):
    """
    Custom QuerySet model to override the base one
    """

    def future(self, user=None):
        """
        Return the published queryset for future events
        """
        if user and user.is_staff:
            return self.filter(start_at__gte=Now())
    
        return self.published().filter(start_at__gte=Now())

    def past(self, user=None):
        """
        Return the published queryset for past events
        """
        if user and user.is_staff:
            return self.filter(start_at__lt=Now())

        return self.published().filter(start_at__lt=Now())


class Event(TimestampMixin, PublishingMixin, URLMixin):
    """
    Model for creating and storing and event object
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    photo = FilerImageField(
        related_name="%(app_label)s_%(class)s_images",
        on_delete=models.SET_NULL,
        null=True,
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(blank=True, null=True)
    intro = models.CharField(max_length=255)
    content = PlaceholderField(slotname="event_content", related_name="event_content")
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name="Tags",
        related_name="%(app_label)s_%(class)s_tags",
        blank=True,
    )
    address = models.CharField(max_length=255, blank=True)
    location = models.ForeignKey(
        to=Location, null=True, on_delete=models.SET_NULL, related_name="events"
    )
    cta_text = models.CharField(max_length=255, blank=True)

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ["start_at"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        """
        Returns the string representation of the event object
        """
        return self.title

    def get_absolute_url(self):
        """
        Builds the url for the event object
        """
        return reverse("events:detail", kwargs={"slug": self.slug})
