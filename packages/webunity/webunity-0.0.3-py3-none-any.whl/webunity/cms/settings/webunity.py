from django.db import models
from wagtail.contrib.settings.models import BaseSetting
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailsvg.blocks import SvgChooserBlock

from webunity.bakery.tasks import build
from webunity.loader import get_model
from webunity.cms import constants

Form = get_model('cms', 'Form')


class AFounders(Orderable):
    settings = ParentalKey("WebspaceSettings", related_name="founders")
    name = models.CharField(default='', blank=True, max_length=100)
    gender = models.CharField(choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
    ], default='', blank=True, max_length=100)
    same_as = models.URLField(blank=True)
    nationality = models.CharField(default='', blank=True, max_length=100)

    general_panels = [
        FieldPanel('name'),
        FieldPanel('gender'),
        FieldPanel('same_as'),
        FieldPanel('nationality'),
    ]

    class Meta:
        verbose_name = 'Founder'
        abstract = True
        app_label = 'cms'


class AWebspaceSettings(BaseSetting, ClusterableModel):
    facebook = models.URLField(blank=True, help_text='Facebook page URL')
    instagram = models.URLField(blank=True, help_text='Instagram page URL')
    linkedin = models.URLField(blank=True, help_text='Linkedin page URL')
    twitter = models.URLField(blank=True, help_text='Twitter page URL')
    pinterest = models.URLField(blank=True, help_text='Pinterest page URL')
    youtube = models.URLField(blank=True, help_text='Youtube page URL')

    brand_name = models.CharField(default='', blank=True, max_length=100)
    brand_short_name = models.CharField(default='', blank=True, max_length=100)
    brand_description = models.TextField(default='', blank=True)

    primary_color_uks = models.CharField(default='', blank=True, max_length=20)
    primary_bg_color = models.CharField(default='', blank=True, max_length=20)
    primary_inverse_color_uks = models.CharField(default='', blank=True, max_length=20)
    primary_inverse_bg_color = models.CharField(default='', blank=True, max_length=20)
    secondary_color_uks = models.CharField(default='', blank=True, max_length=20)
    secondary_bg_color = models.CharField(default='', blank=True, max_length=20)
    secondary_inverse_color_uks = models.CharField(default='', blank=True, max_length=20)
    secondary_inverse_bg_color = models.CharField(default='', blank=True, max_length=20)

    logo_header_primary = StreamField([
        ('image', ImageChooserBlock(label="Image - ratio 200x55")),
        ('svg', SvgChooserBlock(label="Svg - ratio 200x55")),
    ], blank=True)
    logo_header_secondary = StreamField([
        ('image', ImageChooserBlock(label="Image - ratio 200x55")),
        ('svg', SvgChooserBlock(label="Svg - ratio 200x55")),
    ], blank=True)

    logo_schema = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo Entreprise",
        help_text="Logo pour les Schemas Google"
    )
    favicon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Favicon",
    )
    ga_code = models.CharField(
        default='',
        blank=True,
        max_length=100,
        help_text="Google Analytics - Code de suivis"
    )


    vat_id = models.CharField(default='', blank=True, max_length=100)
    legal_name = models.CharField(default='', blank=True, max_length=100)
    founding_date = models.DateField(blank=True, default=None, null=True)
    contact_phone = models.CharField(default='', blank=True, max_length=100)
    contact_email = models.CharField(default='', blank=True, max_length=100)
    area_served = models.CharField(default='', blank=True, max_length=100)
    location_street_address = models.CharField(default='', blank=True, max_length=100)
    location_address_locality = models.CharField(default='', blank=True, max_length=100)
    location_postal_code = models.CharField(default='', blank=True, max_length=100)
    location_address_country = models.CharField(default='', blank=True, max_length=100)
    founding_location = models.CharField(default='', blank=True, max_length=100)





    general_panels = [
        FieldPanel('ga_code'),
    ]

    socials_panels = [
        FieldPanel('facebook'),
        FieldPanel('instagram'),
        FieldPanel('linkedin'),
        FieldPanel('twitter'),
        FieldPanel('youtube'),
        FieldPanel('pinterest'),
    ]

    brand_tab_panels = [
        FieldPanel('brand_name'),
        FieldPanel('brand_short_name'),
        FieldPanel('brand_description'),

        FieldPanel('primary_color_uks'),
        FieldPanel('primary_bg_color'),
        FieldPanel('primary_inverse_color_uks'),
        FieldPanel('primary_inverse_bg_color'),

        FieldPanel('secondary_color_uks'),
        FieldPanel('secondary_bg_color'),
        FieldPanel('secondary_inverse_color_uks'),
        FieldPanel('secondary_inverse_bg_color'),

        StreamFieldPanel('logo_header_primary'),
        StreamFieldPanel('logo_header_secondary'),
        ImageChooserPanel('favicon'),
        ImageChooserPanel('logo_schema'),
    ]

    organization_panels = [
        FieldPanel('vat_id'),
        FieldPanel('legal_name'),
        FieldPanel('founding_date'),
        FieldPanel('contact_phone'),
        FieldPanel('contact_email'),
        FieldPanel('area_served'),
        FieldPanel('location_street_address'),
        FieldPanel('location_address_locality'),
        FieldPanel('location_postal_code'),
        FieldPanel('location_address_country'),
        FieldPanel('founding_location'),
        InlinePanel("founders", label="Founders")
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading='General'),
        ObjectList(brand_tab_panels, heading='Brand'),
        ObjectList(organization_panels, heading='Organization'),
        ObjectList(socials_panels, heading='Socials'),
    ])

    class Meta:
        verbose_name = 'Base'
        abstract = True
        app_label = 'cms'

    @property
    def locale(self):
        return constants.LOCALES[self.language] if self.language in constants.LOCALES else ''

    def save(self, with_build=True, *args, **kwargs):
        super().save(*args, **kwargs)
        if with_build:
            build.delay()
