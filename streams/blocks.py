from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True,help_text='Add Your Title')
    text = blocks.TextBlock(required=True,help_text='Add Some Text')

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class RichTextBlock(blocks.RichTextBlock):

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Full RichText"


class CardBLock(blocks.StructBlock):

    title = blocks.CharBlock(required=True,help_text='Add Your Title')
    
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image",ImageChooserBlock(required=True)),
                ("title",blocks.CharBlock(required=True,max_length=40)),
                ("text",blocks.TextBlock(required=True,max_length=200)),
                ("button_url",blocks.URLBlock(required=False)),

            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "card"
        label = "Card BLock"


class CTABlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True,max_length=60)
    text = blocks.RichTextBlock(required=True,features=["bold","italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.TextBlock(required=True,default='Learn More',max_length=40 )

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"



class ButtonBlock(blocks.StructBlock):

    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)

    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"