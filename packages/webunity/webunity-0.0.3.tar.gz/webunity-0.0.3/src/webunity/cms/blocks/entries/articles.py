from wagtail.core import blocks

from webunity.cms import constants
from webunity.cms.blocks.common import EntryBlock


class ArticlesEntry(EntryBlock):
    articles = blocks.StreamBlock(
        [
            ('article', blocks.PageChooserBlock(required=False, target_model='cms.BlogPage')),
        ],
        min_num=1
    )

    class Meta:
        template = '%s/entries/articles.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Articles"
        icon = 'grip'
