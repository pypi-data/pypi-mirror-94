from wagtail.core import blocks


from webunity.cms import constants
from webunity.cms.blocks.common import \
    SvgBlock, \
    ImageBlock, \
    EntryBlock


class SvgLabel(SvgBlock):
    label = blocks.CharBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    link = blocks.URLBlock(required=False)


class ImageLabel(ImageBlock):
    label = blocks.CharBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    link = blocks.URLBlock(required=False)


class MediasLineEntry(EntryBlock):
    medias = blocks.StreamBlock(
        [
            ('svg_label', SvgLabel()),
            ('image_label', ImageLabel()),
        ],
        min_num=1
    )

    def mock(self, nb_media=6, *args, **kwargs):
        if 'theme' in kwargs:
            icon = self.SVG_ICON_LIGHT \
                if kwargs['theme'] == constants.THEME_LIGHT else self.SVG_ICON_SPACE
        else:
            icon = self.SVG_ICON_SPACE
        media = {
            'type': 'svg_label',
            'value': {
                'file': self.file(icon).id,
                'label': self.h,
            }
        }
        i = 0
        medias = []
        while i < nb_media:
            medias.append(media)
            i += 1
        self.mock_data.update({
            'type': 'medias_line',
            'value': {
                'medias': medias
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/medias_line.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Medias Line"
        icon = 'grip'
