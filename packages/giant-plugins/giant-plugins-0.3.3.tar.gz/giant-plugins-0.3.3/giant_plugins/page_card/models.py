from django.db import models

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from mixins.models import URLMixin
from giant_plugins.utils import RichTextField


class PageCardBlock(CMSPlugin):
    """
    Model for the page card block plugin
    """

    LAYOUT_STACKED = "stacked"
    LAYOUT_LEFT_RIGHT = "left_right"
    LAYOUT_CHOICES = ((LAYOUT_STACKED, "Stacked"), (LAYOUT_LEFT_RIGHT, "Left/Right"))

    layout = models.CharField(
        max_length=255, choices=LAYOUT_CHOICES, default=LAYOUT_LEFT_RIGHT
    )

    title = RichTextField(blank=True)

    def __str__(self):
        """
        String representation of the object
        """
        return f"Page card container {self.pk}"


class PageCard(CMSPlugin, URLMixin):
    """
    A model for an individual page card
    """

    title = models.CharField(max_length=255)
    summary = models.CharField(
        max_length=140, blank=True, help_text="Limited to 140 characters"
    )
    image = FilerImageField(related_name="+", on_delete=models.SET_NULL, null=True, blank=True)
    cta_text = models.CharField(max_length=50, default="Read more")

    def __str__(self):
        """
        String representation of the object
        """
        return f"Page Card #{self.pk}"
