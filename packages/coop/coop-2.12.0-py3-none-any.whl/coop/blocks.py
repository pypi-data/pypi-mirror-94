from django.utils.safestring import mark_safe
from wagtail.core import blocks


class UnwrappedStreamBlock(blocks.StreamBlock):
    """Removes the surrounding divs around streamblocks."""
    def render_basic(self, value, context=None):
        return mark_safe('\n'.join(
            child.render(context=context) for child in value))
