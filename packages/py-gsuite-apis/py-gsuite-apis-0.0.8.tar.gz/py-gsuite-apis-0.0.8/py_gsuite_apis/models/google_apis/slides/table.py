from typing import Optional, List

from pydantic import BaseModel

from py_gsuite_apis.models.google_apis.slides.enums import PropertyState, DashStyle, ContentAlignment
from py_gsuite_apis.models.google_apis.slides.other import Dimension, SolidFill, TextContent


class TableBorderFill(BaseModel):
    solidFill: Optional[SolidFill]


class TableBorderProperties(BaseModel):
    tableBorderFill: Optional[TableBorderFill]
    weight: Optional[Dimension]
    dashStyle: Optional[DashStyle]


class TableCellLocation(BaseModel):
    rowIndex: Optional[int]
    columnIndex: Optional[int]


class TableBorderCell(BaseModel):
    location: Optional[TableCellLocation]
    tableBorderProperties: Optional[TableBorderProperties]


class TableBorderRow(BaseModel):
    tableBorderCells: List[TableBorderCell] = []


class TableCellBackgroundFill(BaseModel):
    propertyState: Optional[PropertyState]
    solidFill: Optional[SolidFill]


class TableCellProperties(BaseModel):
    tableCellBackgroundFill: Optional[TableCellBackgroundFill]
    contentAlignment: Optional[ContentAlignment]


class TableCell(BaseModel):
    location: Optional[TableCellLocation]
    rowSpan: Optional[int]
    columnSpan: Optional[int]
    text: Optional[TextContent]
    tableCellProperties: Optional[TableCellProperties]


class TableRowProperties(BaseModel):
    minRowHeight: Optional[Dimension]


class TableColumnProperties(BaseModel):
    columnWidth: Optional[Dimension]


class TableRow(BaseModel):
    rowHeight: Optional[Dimension]
    tableRowProperties: Optional[TableRowProperties]
    tableCells: List[TableCell] = []


class GoogleSlidesTable(BaseModel):
    rows: Optional[int]
    columns: Optional[int]
    tableRows: List[TableRow] = []
    tableColumns: List[TableColumnProperties] = []
    horizontalBorderRows: List[TableBorderRow] = []
    verticalBorderRows: List[TableBorderRow] = []
