from typing import Optional, List

from pydantic import BaseModel, root_validator

from py_gsuite_apis.models.google_apis.slides.other import Size, AffineTransform
from py_gsuite_apis.models.google_apis.slides.enums import PredefinedLayout, ShapeType, LinkingMode
from py_gsuite_apis.models.google_apis.slides.shape import Placeholder
from py_gsuite_apis.models.google_apis.slides.table import TableCellLocation

"""
Update Presentation Requests
"""

"""
Mixins
"""


class ObjectIdMixin(BaseModel):
    objectId: Optional[str]


"""
Common
"""


class PageElementProperties(BaseModel):
    """
    Common properties for a page element.

    Note: When you initially create a PageElement,
    the API may modify the values of both size and transform ,
    but the visual size will be unchanged.
    """

    pageObjectId: Optional[str]
    size: Optional[Size]
    transform: Optional[AffineTransform]


class SubstringMatchCriteria(BaseModel):
    """
    A criteria that matches a specific string of text in a shape or table.
    """

    text: Optional[str]
    matchCase: Optional[bool]


"""
Charts
"""


class CreateSheetsChartRequestBody(ObjectIdMixin):
    elementProperties: Optional[PageElementProperties]
    spreadsheetId: Optional[str]
    chartId: Optional[int]
    linkingMode: Optional[LinkingMode]


class CreateSheetsChartRequest(ObjectIdMixin):
    """
    Creates an embedded Google Sheets chart.
    """

    createSheetsChart: CreateSheetsChartRequestBody


class ReplaceAllShapesWithSheetsChartRequestBody(BaseModel):
    containsText: Optional[SubstringMatchCriteria]
    spreadsheetId: Optional[str]
    chartId: Optional[int]
    linkingMode: Optional[LinkingMode]
    pageObjectIds: List[str] = []


class ReplaceAllShapesWithSheetsChartRequest(BaseModel):
    """
    Replaces all shapes that match the given criteria with the provided Google Sheets chart.
    The chart will be scaled and centered to fit within the bounds of the original shape.
    """

    replaceAllShapesWithSheetsChart: ReplaceAllShapesWithSheetsChartRequestBody


"""
Table Requests
"""


class TableRange(BaseModel):
    location: Optional[TableCellLocation]
    rowSpan: Optional[int]
    columnSpan: Optional[int]


class InsertTextRequestBody(ObjectIdMixin):
    """
    Insert text into shape or table
    """

    cellLocation: Optional[TableCellLocation]
    text: Optional[str]
    insertionIndex: Optional[int]


class InsertTextIntoTableRequest(BaseModel):
    insertText: InsertTextRequestBody


class InsertTableRowsRequestBody(BaseModel):
    tableObjectId: Optional[str]
    cellLocation: Optional[TableCellLocation]
    insertBelow: Optional[bool]
    number: Optional[int]


class InsertTableRowsRequest(BaseModel):
    insertTableRows: InsertTableRowsRequestBody


class InsertTableColumnsRequestBody(BaseModel):
    tableObjectId: Optional[str]
    cellLocation: Optional[TableCellLocation]
    insertRight: Optional[bool]
    number: Optional[int]


class InsertTableColumnsRequest(BaseModel):
    insertTableColumns: InsertTableColumnsRequestBody


class CreateTableRequestBody(ObjectIdMixin):
    elementProperties: Optional[PageElementProperties]
    rows: Optional[int]
    columns: Optional[int]


class CreateTableRequest(ObjectIdMixin):
    createTable: CreateTableRequestBody


"""
Shapes
"""


class CreateShapeRequest(ObjectIdMixin):
    """"""

    elementProperties: Optional[PageElementProperties]
    shapeType: Optional[ShapeType]


"""
Text
"""


class ReplaceAllTextRequestBody(BaseModel):
    """
    Replace all text on a given presentation
    """

    replaceText: Optional[str]
    pageObjectIds: Optional[str]
    containsText: Optional[SubstringMatchCriteria]


class ReplaceAllTextRequest(BaseModel):
    replaceAllText: ReplaceAllTextRequestBody


"""
Layout
"""


class LayoutReference(BaseModel):
    """
    Slide layout reference. This may reference either:

    - A predefined layout
    - One of the layouts in the presentation.
    """

    predefinedLayout: Optional[PredefinedLayout]
    layoutId: Optional[str]

    @root_validator
    def only_one(cls, values):
        if len([v for v in values.values() if v]) == 1:
            return values

        raise ValueError("You must choose only one from predefinedLayout and layoutId - not both")


class LayoutPlaceholderIdMapping(ObjectIdMixin):
    """
    The user-specified ID mapping for a placeholder that will be created on a slide from a specified layout.
    """

    layoutPlaceholder: Optional[Placeholder]
    layoutPlaceholderObjectId: Optional[str]

    @root_validator
    def only_one(cls, values):
        if len([v for k, v in values.items() if v and k in ["layoutPlaceholder", "layoutPlaceholderObjectId"]]) == 1:
            return values

        raise ValueError("You must choose only one from predefinedLayout and layoutId - not both")


"""
Slides
"""


class CreateSlideRequest(ObjectIdMixin):
    """
    Create a New Slide
    """

    insertionIndex: Optional[int]
    slideLayoutReference: Optional[LayoutReference]
    placeholderIdMappings: Optional[LayoutPlaceholderIdMapping]


class DeleteSlideRequest(ObjectIdMixin):
    """
    Delete a slide
    """

    pass
