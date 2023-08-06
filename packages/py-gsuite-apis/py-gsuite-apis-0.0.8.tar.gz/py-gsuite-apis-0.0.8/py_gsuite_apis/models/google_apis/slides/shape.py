from typing import Optional

from pydantic import BaseModel

from py_gsuite_apis.models.google_apis.slides.enums import PropertyState, ShapeType, ContentAlignment
from py_gsuite_apis.models.google_apis.slides.other import Outline, Shadow, HyperLink, SolidFill, TextContent


class Placeholder(BaseModel):
    """
    The placeholder information that uniquely identifies a placeholder shape.
    """

    type: Optional[ShapeType]
    index: Optional[int]
    parentObjectId: Optional[int]


class ShapeBackgroundFill(BaseModel):
    propertyState: Optional[PropertyState]
    solidFill: Optional[SolidFill]


class ShapeProperties(BaseModel):
    """
    The properties of a Shape .

    If the shape is a placeholder shape as determined by the placeholder field, then these
    properties may be inherited from a parent placeholder shape. Determining the rendered value
    of the property depends on the corresponding propertyState field value.

    Any text autofit settings on the shape are automatically deactivated by requests that can
    impact how text fits in the shape.
    """

    shapeBackgroundFill: Optional[ShapeBackgroundFill]
    outline: Optional[Outline]
    shadow: Optional[Shadow]
    link: Optional[HyperLink]
    contentAlignment: Optional[ContentAlignment]


class GoogleSlidesShape(BaseModel):
    """
    A PageElement kind representing a generic shape that does not have a more specific classification.
    """

    shapeType: Optional[ShapeType]
    text: Optional[TextContent]
    shapeProperties: Optional[ShapeProperties]
    placeholder: Optional[Placeholder]
