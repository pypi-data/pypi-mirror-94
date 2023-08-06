from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
from wagtail.admin.edit_handlers import MultiFieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.utils import camelcase_to_underscore
from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable, Site

from wagtailyoast.edit_handlers import YoastPanel
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList

from webunity.cms import constants
from webunity.cms.blocks.schemas import HowTo, FAQPage
from webunity.loader import get_model, get_class

#  Classes

ArticlesEntry = get_class('cms.blocks.entries', 'ArticlesEntry')
ButtonsEntry = get_class('cms.blocks.entries', 'ButtonsEntry')
CardsEntry = get_class('cms.blocks.entries', 'CardsEntry')
EmbedEntry = get_class('cms.blocks.entries', 'EmbedEntry')
GridInfoEntry = get_class('cms.blocks.entries', 'GridInfoEntry')
ImageEntry = get_class('cms.blocks.entries', 'ImageEntry')
ComponentTextEntry = get_class('cms.blocks.entries', 'ComponentTextEntry')
MediasLineEntry = get_class('cms.blocks.entries', 'MediasLineEntry')
SvgEntry = get_class('cms.blocks.entries', 'SvgEntry')
TextEntry = get_class('cms.blocks.entries', 'TextEntry')
TimeLineEntry = get_class('cms.blocks.entries', 'TimeLineEntry')
CalendlyEntry = get_class('cms.blocks.entries', 'CalendlyEntry')
TableEntry = get_class('cms.blocks.entries', 'TableEntry')
NumbersEntry = get_class('cms.blocks.entries', 'NumbersEntry')
AccordionEntry = get_class('cms.blocks.entries', 'AccordionEntry')
FormEntry = get_class('cms.blocks.entries', 'FormEntry')
GalleryEntry = get_class('cms.blocks.entries', 'GalleryEntry')
StreamContentEntry = get_class('cms.blocks.entries', 'StreamContentEntry')
GallerySliderEntry = get_class('cms.blocks.entries', 'GallerySliderEntry')

#  Models
Menu = get_model('cms', 'Menu')
IconSnippet = get_model('cms', 'IconSnippet')
Navigation = get_model('cms', 'Navigation')


class AGenericPage(Page):
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="SEO - Image",
    )

    theme = models.CharField(
        choices=constants.THEME_CHOICES,
        default=constants.THEME_SPACE,
        max_length=100,
        help_text="Permet de changer le theme du header et du footer"
    )

    breadcrumb = models.BooleanField(
        default=True,
        verbose_name="Public pour Google",
        help_text="Ajoute la page dans le sitemap et génère un schéma Breadcrumb",
    )

    schemas = StreamField([
        ('how_to', HowTo()),
        ('faq_page', FAQPage()),
    ], blank=True)

    navigation = models.ForeignKey(
        Navigation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Navigation",
    )

    keywords = models.CharField(default='', blank=True, max_length=100)

    body = StreamField([
        ('svg', SvgEntry()),
        ('image', ImageEntry()),
        ('text', TextEntry()),
        ('cards', CardsEntry()),
        ('component_text', ComponentTextEntry()),
        ('grid_info', GridInfoEntry()),
        ('medias_line', MediasLineEntry()),
        ('timeline', TimeLineEntry()),
        ('buttons', ButtonsEntry()),
        ('calendly', CalendlyEntry()),
        ('articles', ArticlesEntry()),
        ('embed', EmbedEntry()),
        ('table', TableEntry()),
        ('accordion', AccordionEntry()),
        ('numbers', NumbersEntry()),
        ('form', FormEntry()),
        ('gallery', GalleryEntry()),
        ('gallery_slider', GallerySliderEntry()),
        ('stream_content', StreamContentEntry()),
    ], blank=True)

    content_panels = [
        StreamFieldPanel('body'),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], "Google Search"),
        MultiFieldPanel([
            ImageChooserPanel('feed_image'),
            FieldPanel('breadcrumb'),
        ], "SEO - DATA"),
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('theme'),
        SnippetChooserPanel('navigation'),
    ]

    subpage_types = [
        'cms.ContentPage',
        'cms.DocumentPage',
        'cms.BlogPage',
    ]

    class Meta:
        abstract = True
        app_label = 'cms'

    def get_context(self, request, *args, **kwargs):
        context = super(AGenericPage, self).get_context(request)
        context['debug'] = settings.DEBUG
        context['icons'] = IconSnippet.get_context()
        context['version'] = settings.VERSION
        context['site'] = Site.find_for_request(request)
        context['studio'] = {
            'name': constants.STUDIO_NAME,
            'email': constants.STUDIO_EMAIL,
            'url': constants.STUDIO_URL,
        }
        return context

    @cached_property
    def get_breadcrumbs(self):
        #  FIXME: filter by `breadcrumb` seem not to be possible with wagtail Page
        ret = []
        items = self.get_children().type(AGenericPage).specific().live()
        for item in items:
            if item.breadcrumb:
                ret.append(item)
        return ret

    def get_sitemap_urls(self, request=None):
        if not self.breadcrumb:
            return []
        urls = super().get_sitemap_urls(request)
        # TODO: here
        """
        if self.language_pages:
            urls[-1]['alternatives'] = []
            for language_page in self.language_pages.all():
                urls[-1]['alternatives'].append({
                    'language': language_page.language,
                    'href': language_page.page.get_full_url(),
                })
        """
        return urls

    def get_template(self, request, *args, **kwargs):
        return "%s/%s.html" % (
            constants.PAGES_TEMPLATES_PATH,
            camelcase_to_underscore(self.__class__.__name__)
        )
