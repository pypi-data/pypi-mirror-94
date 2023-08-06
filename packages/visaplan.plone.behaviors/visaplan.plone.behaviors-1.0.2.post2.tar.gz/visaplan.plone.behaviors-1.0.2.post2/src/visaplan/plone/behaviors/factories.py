"""\
visaplan.plone.behaviors: schemas for Dexterity-based content types

The schemas reflect fields which are currently implemented one-by-one
for the Archetypes-based content types of the UNITRACC family of Plone sites.
"""
from zope.interface import implementer

from .interfaces import (
    IHeightAndWidth,
    ICaptionAndLegend,
    IExcludeFromSearch,
    IPreviewImage,
    IHierarchicalBuzzword,
    )


@implementer(IHeightAndWidth)
class HeightAndWidth(object):
    """
    factory class for IHeightAndWidth
    """

    def __init__(self, context):
        self.context = context

    @property
    def height(self):
        return getattr(self.context, '_height', None)

    @height.setter
    def height(self, value):
        self.context._height = value

    @property
    def width(self):
        return getattr(self.context, '_width', None)

    @width.setter
    def width(self, value):
        self.context._width = value


@implementer(ICaptionAndLegend)
class CaptionAndLegend(object):
    """
    factory class for ICaptionAndLegend
    """

    def __init__(self, context):
        self.context = context

    @property
    def caption(self):
        return getattr(self.context, '_caption', None)

    @caption.setter
    def caption(self, value):
	if value is not None:
	    value = value.strip()
        self.context._caption = value

    @property
    def legend(self):
        return getattr(self.context, '_legend', None)

    @legend.setter
    def legend(self, value):
	if value is not None:
	    value = value.strip()
        self.context._legend = value


@implementer(IExcludeFromSearch)
class ExcludeFromSearch(object):
    """
    factory class for IExcludeFromSearch
    """

    def __init__(self, context):
        self.context = context

    @property
    def excludeFromSearch(self):
        return getattr(self.context, '_excludeFromSearch', False)

    @excludeFromSearch.setter
    def excludeFromSearch(self, value):
        self.context._excludeFromSearch = value


@implementer(IPreviewImage)
class PreviewImage(object):
    """
    factory class for IPreviewImage
    """

    def __init__(self, context):
        self.context = context

    @property
    def image(self):
        return self.context.image
        return getattr(self.context, 'image', None)

    @image.setter
    def image(self, value):
        self.context.image = value

    def getThumbnailPath(self):
        """
        Return the TTW path to the (freely accessible) preview image
        """
        #TODO: Use the image attribute to
        #      create a scaled preview image
        #      and save it in the filesystem
        #      (where an Apache server etc. can be configured to serve it
        #      and all of its siblings in a generic way)
        return self.getDefaultThumbnailPath()

    def buildStaticImagePath(self, name):
        # TTW path of the given default image name;
        # override this to use another virtual base
        return ('/++resource++unitracc-images/%(name)s'
                % locals())

    def getDefaultThumbnailPath(self):
        return self.buildStaticImagePath('picto_media_animation_m.png')


@implementer(IHierarchicalBuzzword)
class HierarchicalBuzzword(object):
    """
    factory class for IHierarchicalBuzzword
    """

    def __init__(self, context):
        self.context = context

    @property
    def code(self):
        return getattr(self.context, '_code', None)

    @code.setter
    def code(self, value):
	if value is not None:
	    value = value.strip()
        self.context._code = value
