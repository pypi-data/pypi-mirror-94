from __future__ import annotations

from typing import Optional, List, Union

from pydantic import BaseModel, root_validator

from py_gsuite_apis.models.google_apis.slides.shape import GoogleSlidesShape
from py_gsuite_apis.models.google_apis.slides.image import GoogleSlidesImage
from py_gsuite_apis.models.google_apis.slides.video import GoogleSlidesVideo
from py_gsuite_apis.models.google_apis.slides.table import GoogleSlidesTable

from py_gsuite_apis.models.google_apis.slides.enums import PageType, PropertyState, ThemeColorType
from py_gsuite_apis.models.google_apis.slides.other import (
    OpaqueColor,
    SolidFill,
    Size,
    AffineTransform,
    RgbColor,
    ImageProperties,
)

"""
Pages
"""


"""
Colors and Sizes
"""


class StretchedPictureFill(BaseModel):
    """"""

    contentUrl: Optional[str]
    size: Optional[Size]


class PageBackgroundFill(BaseModel):
    """
    The page background fill.
    """

    propertyState: Optional[PropertyState]
    # UNION FIELDS
    solidFill: Optional[SolidFill]
    stretchedPictureFill: Optional[StretchedPictureFill]
    # END UNION FIELDS

    @root_validator
    def only_one_fill(cls, values):
        if len([v for k, v in values.items() if v and k in ["solidFill", "stretchedPictureFill"]]) == 2:
            raise ValueError("You must choose only one from solidFill and stretchedPictureFill.")

        if len([v for k, v in values.items() if v and k in ["solidFill", "stretchedPictureFill"]]) == 1:
            return values

        # Default to white background fill
        return {
            "propertyState": values["propertyState"],
            "solidFill": SolidFill(
                color=OpaqueColor(
                    rgbColor=RgbColor(red=255, green=255, blue=255),
                    # nothing else goes here?
                ),
                alpha=1,
            ),
        }


class ThemeColorPair(BaseModel):
    """"""

    type: Optional[ThemeColorType]
    color: Optional[RgbColor]


class ColorScheme(BaseModel):
    """"""

    colors: List[ThemeColorPair] = []


"""
Slides Charts
"""


class SheetsChartProperties(BaseModel):
    chartImageProperties: Optional[ImageProperties]


class GoogleSlidesSheetsChart(BaseModel):
    spreadsheetId: Optional[str]
    chartId: Optional[int]
    contentUrl: Optional[str]
    sheetsChartProperties: Optional[SheetsChartProperties]


"""
Properties
"""


class LayoutProperties(BaseModel):
    """
    The properties of Page are only relevant for pages with pageType LAYOUT.
    """

    name: Optional[str]
    displayName: Optional[str]
    masterObjectId: Optional[str]


class NotesProperties(BaseModel):
    """
    The properties of Page that are only relevant for pages with pageType NOTES.
    """

    speakerNotesObjectId: Optional[str]


class PageProperties(BaseModel):
    """
    The properties of the Page.

    The page will inherit properties from the parent page.
    Depending on the page type the hierarchy is defined in either SlideProperties or LayoutProperties.
    """

    pageBackgroundFill: Optional[PageBackgroundFill]
    colorScheme: Optional[ColorScheme]


class MasterProperties(BaseModel):
    """
    he properties of Page that are only relevant for pages with pageType MASTER.
    """

    displayName: Optional[str]


"""
Page Elements
"""


class GoogleSlidesWordArt(BaseModel):
    """
    A PageElement kind representing word art.
    """

    renderedText: Optional[str]


class GoogleSlidesPageElementBase(BaseModel):
    """
    Base model for a visual element rendered on a page.
    """

    objectId: Optional[str]
    title: Optional[str]
    description: Optional[str]
    size: Optional[Size]
    transform: Optional[AffineTransform]


GoogleSlidesPageElementBase.update_forward_refs()


class GoogleSlidesPageElementShape(GoogleSlidesPageElementBase):
    shape: GoogleSlidesShape


class GoogleSlidesPageElementImage(GoogleSlidesPageElementBase):
    image: GoogleSlidesImage


class GoogleSlidesPageElementVideo(GoogleSlidesPageElementBase):
    video: GoogleSlidesVideo


class GoogleSlidesPageElementTable(GoogleSlidesPageElementBase):
    table: GoogleSlidesTable


class GoogleSlidesPageElementWordArt(GoogleSlidesPageElementBase):
    wordArt: GoogleSlidesWordArt


class GoogleSlidesPageElementSheetsChart(GoogleSlidesPageElementBase):
    sheetsChart: GoogleSlidesSheetsChart


GoogleSlidesPageElement = Union[
    GoogleSlidesPageElementShape,
    Union[
        GoogleSlidesPageElementImage,
        Union[
            GoogleSlidesPageElementVideo,
            Union[
                GoogleSlidesPageElementTable,
                Union[
                    GoogleSlidesPageElementWordArt,
                    GoogleSlidesPageElementSheetsChart,
                    # Union[
                    #     GoogleSlidesPageElementSheetsChart,
                    #     GoogleSlidesPageElementGroup,
                    # ]
                ],
            ],
        ],
    ],
]


class GoogleSlidesPageElementGroup(GoogleSlidesPageElementBase):
    """
    A PageElement kind representing a joined collection of PageElements.
    """

    # children: List[GoogleSlidesPageElement] = []
    children: List[Union[GoogleSlidesPageElement, GoogleSlidesPageElementGroup]] = []


GoogleSlidesPageElementGroup.update_forward_refs()


class GoogleSlidesNotesPage(BaseModel):
    """
    Only duplicated here to prevent circular dependecies
    """

    objectId: Optional[str]
    revisionId: Optional[str]
    pageType: Optional[PageType]
    pageElements: List[Union[GoogleSlidesPageElement, GoogleSlidesPageElementGroup]] = []
    pageProperties: Optional[PageProperties]
    notesProperties: Optional[NotesProperties]


class SlideProperties(BaseModel):
    """
    The properties of Page that are only relevant for pages with pageType SLIDE.
    """

    layoutObjectId: Optional[str]
    masterObjectId: Optional[str]
    notesPage: Optional[GoogleSlidesNotesPage]


SlideProperties.update_forward_refs()


class GoogleSlidesPage(BaseModel):
    objectId: Optional[str]
    revisionId: Optional[str]
    pageType: Optional[PageType]
    pageElements: List[Union[GoogleSlidesPageElement, GoogleSlidesPageElementGroup]] = []
    pageProperties: Optional[PageProperties]
    # UNION FIELDS
    slideProperties: Optional[SlideProperties]
    layoutProperties: Optional[LayoutProperties]
    notesProperties: Optional[NotesProperties]
    masterProperties: Optional[MasterProperties]
    # END UNION FIELDS

    @root_validator
    def valid_properties(cls, values):
        properties_values = [
            v
            for k, v in values.items()
            if v and k in ["slideProperties", "layoutProperties", "notesProperties", "masterProperties"]
        ]

        # Seems like some responses have no page type or properties. I'll roll with it, Google.
        # if len(properties_values) == 0:
        #     raise ValueError(f"No properties provided for slides page with type: {values['pageType']}!")

        # make sure request has correct property field
        propertyField = {
            "SLIDE": "slideProperties",
            "MASTER": "masterProperties",
            "LAYOUT": "layoutProperties",
            "NOTES": "notesProperties",
            "NOTES_MASTER": "notesProperties",
        }.get(values.get("pageType"))

        # if only one selected, as long as its the correct one, we're good to go
        if len(properties_values) == 1:
            # hmmmm...sometimes the pageType is none, but there is still one properties values - weird
            if values.get("pageType"):
                if not values.get(propertyField):
                    raise ValueError(
                        f"Incorrect matching of properties: {propertyField} to page type: {values.get('pageType')}."
                    )

        if len(properties_values) >= 2:
            error_message = (
                "You must choose only one from slideProperties, layoutProperties,"
                " notesProperties, and masterProperties."
            )
            raise ValueError(error_message)

        return values


GoogleSlidesPage.update_forward_refs()
