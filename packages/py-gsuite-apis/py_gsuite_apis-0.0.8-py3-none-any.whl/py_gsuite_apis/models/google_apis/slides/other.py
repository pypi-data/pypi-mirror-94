from typing import Optional, List, Dict

from pydantic import BaseModel, conint, root_validator

from py_gsuite_apis.models.google_apis.slides.enums import (
    Unit,
    PropertyState,
    ThemeColorType,
    RelativeSlideLink,
    DashStyle,
    ShadowType,
    RecolorName,
    RectanglePosition,
    TextDirection,
    SpacingMode,
    AutoTextType,
    TextAlignment,
)


class Dimension(BaseModel):
    magnitude: Optional[int]
    unit: Optional[Unit]


class AffineTransform(BaseModel):
    """
    AffineTransform uses a 3x3 matrix with an implied last row of [ 0 0 1 ]
    to transform source coordinates (x,y) into destination coordinates (x', y') according to:

    [ x']   [  scaleX  shearX  translateX  ] [ x ]
    [ y'] = [  shearY  scaleY  translateY  ] [ y ]
    [ 1 ]   [      0       0         1     ] [ 1 ]

    After transformation,

    x' = scaleX * x + shearX * y + translateX;
    y' = scaleY * y + shearY * x + translateY;

    This message is therefore composed of these six matrix elements.
    """

    scaleX: Optional[int]
    scaleY: Optional[int]
    shearX: Optional[int]
    shearY: Optional[int]
    translateX: Optional[int]
    translateY: Optional[int]
    unit: Optional[Unit]


class RgbColor(BaseModel):
    """ Representing Color values for Google colors - defaults to black """

    red: Optional[conint(ge=0, le=255)] = 0
    green: Optional[conint(ge=0, le=255)] = 0
    blue: Optional[conint(ge=0, le=255)] = 0


class OpaqueColor(BaseModel):
    """
    A themeable solid color value.
    """

    rgbColor: Optional[RgbColor]
    themeColor: Optional[ThemeColorType]

    @root_validator
    def only_one(cls, values):
        if len([v for v in values.values() if v]) == 1:
            return values

        raise ValueError("You must choose one from rgbColor and themeColor - not both")


class HyperLink(BaseModel):
    """
    Hypertext Link
    """

    url: Optional[str]
    relativeLink: Optional[RelativeSlideLink]
    pageObjectId: Optional[str]
    slideIndex: Optional[int]

    @root_validator
    def only_one(cls, values):
        if len([v for v in values.values() if v]) == 1:
            return values

        raise ValueError("You must choose only one from rgbColor and themeColor - not both")


class SolidFill(BaseModel):
    """
    A solid color fill. The page or page element is filled entirely with the specified color value.

    If any field is unset, its value may be inherited from a parent placeholder if it exists.
    """

    color: Optional[OpaqueColor]
    alpha: int = 1


class Size(BaseModel):
    width: Optional[Dimension]
    height: Optional[Dimension]


class OptionalColor(BaseModel):
    opaqueColor: Optional[OpaqueColor]


class WeightedFontFamily(BaseModel):
    fontFamily: Optional[str]
    weight: Optional[int]


class TextStyle(BaseModel):
    """
    Represents the styling that can be applied to a TextRun.

    If this text is contained in a shape with a parent placeholder,
    then these text styles may be inherited from the parent. Which text
    styles are inherited depend on the nesting level of lists:

    - A text run in a paragraph that is not in a list will inherit its text style from the the
      newline character in the paragraph at the 0 nesting level of the list inside the parent placeholder.
    - A text run in a paragraph that is in a list will inherit its text style from the newline character
      in the paragraph at its corresponding nesting level of the list inside the parent placeholder.

    Inherited text styles are represented as unset fields in this message. If text is contained in a
    shape without a parent placeholder, unsetting these fields will revert the style to a value matching
    the defaults in the Slides editor.
    """

    backgroundColor: Optional[OptionalColor]
    foregroundColor: Optional[OptionalColor]
    bold: Optional[bool]
    italic: Optional[bool]
    fontFamily: Optional[str]
    fontSize: Optional[Dimension]
    link: Optional[HyperLink]
    baselineOffset: Optional[OptionalColor]
    weightedFontFamily: Optional[WeightedFontFamily]
    smallCaps: Optional[bool]
    underline: Optional[bool]
    strikethrough: Optional[bool]


class NestingLevel(BaseModel):
    """
    Contains properties describing the look and feel of a list bullet at a given level of nesting.
    """

    bulletStyle: Optional[TextStyle]


class GoogleSlidesList(BaseModel):
    listId: Optional[str]
    # nestingLevel: GoogleSlidesListNestingLevelMapping
    nestingLevel: Dict[int, NestingLevel]


class OutlineFill(BaseModel):
    """
    The fill of the outline
    """

    solidFill: Optional[SolidFill]


class Outline(BaseModel):
    """
    The outline of a PageElement .

    If these fields are unset, they may be inherited from a parent placeholder if it exists.
    If there is no parent, the fields will default to the value used for new page elements created
    in the Slides editor, which may depend on the page element kind.
    """

    outlineFill: Optional[OutlineFill]
    weight: Optional[Dimension]
    dashStyle: Optional[DashStyle]
    propertState: Optional[PropertyState]


class Shadow(BaseModel):
    """
    The shadow properties of a page element.

    If these fields are unset, they may be inherited from a parent placeholder if it exists.
    If there is no parent, the fields will default to the value used for new page elements
    created in the Slides editor, which may depend on the page element kind.
    """

    type: Optional[ShadowType]
    transform: Optional[AffineTransform]
    alignment: Optional[RectanglePosition]
    blurRadius: Optional[Dimension]
    color: Optional[OpaqueColor]
    alpha: Optional[int]
    rotateWithShape: Optional[bool]
    propertyState: Optional[PropertyState]


class ColorStop(BaseModel):
    """
    A color and position in a gradient band.
    """

    color: Optional[OpaqueColor]
    alpha: Optional[int]
    position: Optional[int]


class Recolor(BaseModel):
    """
    A recolor effect applied on an image
    """

    recolorStops: List[ColorStop] = []
    name: Optional[RecolorName]


class CropProperties(BaseModel):
    """
    The crop properties of an object enclosed in a container. For example, an Image .

    The crop properties is represented by the offsets of four edges which define a crop rectangle.
    The offsets are measured in percentage from the corresponding edges of the object's original
    bounding rectangle towards inside, relative to the object's original dimensions.

    - If the offset is in the interval (0, 1), the corresponding edge of crop rectangle is positioned
      inside of the object's original bounding rectangle.
    - If the offset is negative or greater than 1, the corresponding edge of crop rectangle is positioned
      outside of the object's original bounding rectangle.
    - If the left edge of the crop rectangle is on the right side of its right edge, the object will be
      flipped horizontally.
    - If the top edge of the crop rectangle is below its bottom edge, the object will be flipped vertically.
    - If all offsets and rotation angle is 0, the object is not cropped.

    After cropping, the content in the crop rectangle will be stretched to fit its container.
    """

    leftOffset: Optional[int]
    rightOffset: Optional[int]
    topOffset: Optional[int]
    bottomOffset: Optional[int]
    angle: Optional[conint(ge=0, le=360)]


class ImageProperties(BaseModel):
    """

    """

    cropProperties: Optional[CropProperties]
    transparency: Optional[int]
    brightness: Optional[int]
    constrast: Optional[int]
    recolor: Optional[Recolor]
    outline: Optional[Outline]
    shadow: Optional[Shadow]
    link: Optional[HyperLink]


class Bullet(BaseModel):
    listId: Optional[str]
    nestingLevel: Optional[int]
    glyph: Optional[str]
    bulletStyle: Optional[TextStyle]


class TextRun(BaseModel):
    """

    """

    content: Optional[str]
    style: Optional[TextStyle]


class AutoText(BaseModel):
    type: Optional[AutoTextType]
    content: Optional[str]
    style: Optional[TextStyle]


class ParagraphStyle(BaseModel):
    """
    Styles that apply to a whole paragraph.

    If this text is contained in a shape with a parent placeholder,
    then these paragraph styles may be inherited from the parent. Which
    paragraph styles are inherited depend on the nesting level of lists:

    - A paragraph not in a list will inherit its paragraph style from the paragraph
      at the 0 nesting level of the list inside the parent placeholder.
    - A paragraph in a list will inherit its paragraph style from the paragraph at its
      corresponding nesting level of the list inside the parent placeholder.

    Inherited paragraph styles are represented as unset fields in this message.
    """

    lineSpacing: Optional[int]
    alignment: Optional[TextAlignment]
    indentStart: Optional[Dimension]
    indentEnd: Optional[Dimension]
    spaceAbove: Optional[Dimension]
    spaceBelow: Optional[Dimension]
    indentFirstLine: Optional[Dimension]
    direction: Optional[TextDirection]
    spacingMode: Optional[SpacingMode]


class ParagraphMarker(BaseModel):
    style: Optional[ParagraphStyle]
    bullet: Optional[Bullet]


class TextElement(BaseModel):
    """
    A TextElement describes the content of a range of indices in the text content of a Shape or TableCell.
    """

    startIndex: Optional[int]
    endIndex: Optional[int]
    # UNION FIELDS
    paragraphMarker: Optional[ParagraphMarker]
    textRun: Optional[TextRun]
    autoText: Optional[AutoText]
    # END UNION FIELDS


class TextContent(BaseModel):
    """
    The general text content. The text must reside in a compatible shape
    (e.g. text box or rectangle) or a table cell in a page.
    """

    textElements: List[TextElement] = []
    lists: Dict[str, GoogleSlidesList]
