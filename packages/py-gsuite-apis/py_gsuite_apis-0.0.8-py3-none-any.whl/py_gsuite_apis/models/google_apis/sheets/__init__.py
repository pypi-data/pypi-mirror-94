from typing import List, Optional, Any

from pydantic import BaseModel, root_validator

from py_gsuite_apis.models.google_apis.sheets.charts import GoogleSheetsChart
from py_gsuite_apis.models.google_apis.sheets.other import (
    ExtendedValue,
    GoogleColor,
    GoogleColorStyle,
    GoogleSheetsGridRange,
    BooleanCondition,
    GoogleSheetsTextFormat,
    GoogleSheetsSortSpec,
    GoogleSheetsFilterSpec,
    DataExecutionStatus,
    DataSourceColumn,
    DataSourceColumnReference,
    GoogleSheetsEmbeddedObjectPosition,
)
from py_gsuite_apis.models.google_apis.sheets.enums import (
    SheetType,
    Dimension,
    NumberFormatType,
    BorderStyle,
    VerticalAlign,
    HorizontalAlign,
    WrapStrategy,
    TextDirection,
    HyperlinkDisplayType,
    InterpolationPointType,
    ThemeColorType,
    DataSourceTableColumnSelectionType,
    DeveloperMetadataVisibility,
    DeveloperMetadataLocationType,
)


"""
Cells
"""


class NumberFormat(BaseModel):
    type: Optional[NumberFormatType]
    pattern: Optional[str]


class TextRotation(BaseModel):
    angle: Optional[int]
    vertical: Optional[bool]


class TextFormatRun(BaseModel):
    startIndex: Optional[int]
    format: Optional[GoogleSheetsTextFormat]


class Border(BaseModel):
    style: Optional[BorderStyle]
    width: Optional[int]  # deprecated
    color: Optional[GoogleColor]
    colorStyle: Optional[GoogleColorStyle]


class Borders(BaseModel):
    top: Optional[Border]
    bottom: Optional[Border]
    left: Optional[Border]
    right: Optional[Border]


class Padding(BaseModel):
    top: Optional[int]
    bottom: Optional[int]
    left: Optional[int]
    right: Optional[int]


class DataValidationRule(BaseModel):
    condition: Optional[BooleanCondition]
    inputMessage: Optional[str]
    strict: Optional[bool]
    showCustomUi: Optional[bool]


class DataSourceTable(BaseModel):
    dataSourceId: Optional[str]
    columnSelectionType: Optional[DataSourceTableColumnSelectionType]
    rowLimit: Optional[int]
    columns: List[GoogleSheetsFilterSpec] = []
    sortSpecs: List[GoogleSheetsSortSpec] = []
    dataExecutionStatus: Optional[DataExecutionStatus]


class DataSourceFormula(BaseModel):
    dataSourceId: Optional[str]
    dataExecutionStatus: Optional[DataExecutionStatus]


class CellFormat(BaseModel):
    numberFormat: Optional[NumberFormat]
    backgroundColor: Optional[GoogleColor]
    backgroundColorStyle: Optional[GoogleColorStyle]
    borders: Optional[Borders]
    padding: Optional[Padding]
    horizontalAlignment: Optional[HorizontalAlign]
    verticalAlignment: Optional[VerticalAlign]
    wrapStrategy: Optional[WrapStrategy]
    textDirection: Optional[TextDirection]
    textFormat: Optional[GoogleSheetsTextFormat]
    hyperlinkDisplayType: Optional[HyperlinkDisplayType]
    textRotation: Optional[TextRotation]


class CellData(BaseModel):
    userEnteredValue: Optional[ExtendedValue]
    effectiveValue: Optional[ExtendedValue]
    formattedValue: Optional[str]
    userEnteredFormat: Optional[CellFormat]
    effectiveFormat: Optional[CellFormat]
    hyperlink: Optional[str]
    note: Optional[str]
    textFormatRuns: List[TextFormatRun] = []
    dataValidation: Optional[DataValidationRule]
    # pivotTable: Optional[PivotTable]
    pivotTable: Optional[Any]
    dataSourceTable: Optional[DataSourceTable]
    dataSourceFormula: Optional[DataSourceFormula]


"""
Utility
"""


class SlicerSpec(BaseModel):
    dataRange: Optional[GoogleSheetsGridRange]
    filterCriteria: Optional[Any]
    # filterCriteria: Optional[FilterCriteria]  # deprecated
    columnIndex: Optional[int]
    applyToPivotTables: Optional[bool]
    title: Optional[str]
    textFormat: Optional[GoogleSheetsTextFormat]
    backgroundColor: Optional[GoogleColor]
    backgroundColorStyle: Optional[GoogleColorStyle]
    horizontalAlignment: Optional[HorizontalAlign]


class Slicer(BaseModel):
    sliderId: Optional[int]
    spec: Optional[SlicerSpec]
    position: Optional[GoogleSheetsEmbeddedObjectPosition]


class InterpolationPoint(BaseModel):
    color: Optional[GoogleColor]
    colorStyle: Optional[GoogleColorStyle]
    type: Optional[InterpolationPointType]
    value: Optional[str]


class BooleanRule(BaseModel):
    condition: Optional[BooleanCondition]
    format: Optional[CellFormat]


class GradientRule(BaseModel):
    """
    A rule that applies a gradient color scale format, based on the interpolation points listed
    The format of a cell will vary based on its contents as compared to the values of the interpolation points.
    """

    minpoint: Optional[InterpolationPoint]
    midpoint: Optional[InterpolationPoint]
    maxpoint: Optional[InterpolationPoint]


class ConditionalFormatRule(BaseModel):
    ranges: List[GoogleSheetsGridRange] = []
    booleanRule: Optional[BooleanRule]
    gradientRule: Optional[GradientRule]


class BasicFilter(BaseModel):
    range: Optional[GoogleSheetsGridRange]
    sortSpecs: List[GoogleSheetsSortSpec] = []
    filterSpecs: List[GoogleSheetsFilterSpec] = []
    criteria: Any  # deprecated


class FilterView(BasicFilter):
    filterViewId: Optional[int]
    title: Optional[str]
    namedRangeId: Optional[str]


"""
Ranges
"""


class Editors(BaseModel):
    users: List[str] = []
    groups: List[str] = []
    domainUsersCanEdit: Optional[bool]


class ProtectedRange(BaseModel):
    protectedRangeId: Optional[int]
    namedRangeId: Optional[str]
    range: Optional[GoogleSheetsGridRange]
    description: Optional[str]
    requestingUserCanEdit: Optional[bool]
    unprotectedRanges: List[GoogleSheetsGridRange] = []
    editors: Optional[Editors]


class NamedRange(BaseModel):
    name: Optional[str]
    namedRangeId: Optional[str]
    range: Optional[GoogleSheetsGridRange]


class BandingProperties(BaseModel):
    headerColor: Optional[GoogleColor]
    headerColorStyle: Optional[GoogleColorStyle]
    firstBandColor: Optional[GoogleColor]
    firstBandColorStyle: Optional[GoogleColorStyle]
    secondBandColor: Optional[GoogleColor]
    secondBandColorStyle: Optional[GoogleColorStyle]
    footerColor: Optional[GoogleColor]
    footerColorStyle: Optional[GoogleColorStyle]


class BandedRange(BaseModel):
    bandedRangeId: Optional[int]
    range: Optional[GoogleSheetsGridRange]
    rowProperties: Optional[BandingProperties]
    columnProperties: Optional[BandingProperties]


class DimensionRange(BaseModel):
    sheetId: Optional[int]
    dimension: Optional[Dimension]
    startIndex: Optional[int]
    endIndex: Optional[int]


"""
Developer
"""


class DeveloperMetadataLocation(BaseModel):
    locationType: Optional[DeveloperMetadataLocationType]
    # Union field location can be only one of the following:
    spreadsheet: Optional[bool]
    sheetId: Optional[int]
    dimensionsRange: Optional[DimensionRange]
    # End of list of possible types for union field location.

    @root_validator
    def only_one(cls, values):
        if len([v for k, v in values.items() if v and k in ["spreadsheet", "sheetId", "dimensionsRange"]]) == 1:
            return values

        raise ValueError("You must choose exactly one from spreadsheet, sheetId, and dimensionsRange.")


class DeveloperMetadata(BaseModel):
    metadataId: Optional[int]
    metadataKey: Optional[str]
    metadataValue: Optional[str]
    location: Optional[DeveloperMetadataLocation]
    visibility: Optional[DeveloperMetadataVisibility]


"""
Sheets
"""


class DataSourceSheetProperties(BaseModel):
    dataSourceId: Optional[str]
    columns: List[DataSourceColumn] = []
    dataExecutionStatus: Optional[DataExecutionStatus]


class DimensionProperties(BaseModel):
    hiddenByFilter: bool = False
    hiddenByUser: bool = False
    pixelSize: Optional[int]
    developerMetadata: List[DeveloperMetadata] = []
    dataSourceColumnReference: Optional[DataSourceColumnReference]


class DimensionGroup(BaseModel):
    range: Optional[DimensionRange]
    depth: Optional[int]
    collapsed: bool = False


class RowData(BaseModel):
    values: List[CellData] = []


class GridProperties(BaseModel):
    rowCount: Optional[int]
    columnCount: Optional[int]
    frozenRowCount: Optional[int]
    frozenColumnCount: Optional[int]
    hideGridlines: bool = False
    rowGroupControlAfter: bool = False
    columnGroupControlAfter: bool = False


class GridData(BaseModel):
    startRow: Optional[int]
    startColumn: Optional[int]
    rowData: List[RowData] = []
    rowMetadata: List[DimensionProperties] = []
    columnMetadata: List[DimensionProperties]


class SheetProperties(BaseModel):
    sheetId: str
    title: str
    index: int
    hidden: bool = False
    rightToLeft: bool = False
    tabColor: Optional[GoogleColor]
    tabColorStyle: Optional[GoogleColorStyle]
    sheetType: Optional[SheetType]
    gridProperties: Optional[GridProperties]
    dataSourceSheetProperties: Optional[DataSourceSheetProperties]


class Sheet(BaseModel):
    """
    A sheet in a spreadsheet.
    """

    properties: Optional[SheetProperties]
    data: List[GridData] = []
    merges: List[GoogleSheetsGridRange] = []
    conditionalFormats: List[ConditionalFormatRule] = []
    filterViews: List[FilterView] = []
    protectedRanges: List[ProtectedRange] = []
    basicFilter: Optional[BasicFilter]
    charts: List[GoogleSheetsChart] = []
    bandedRanges: List[BandedRange] = []
    developerMetadata: List[DeveloperMetadata] = []
    rowGroups: List[DimensionGroup] = []
    columnGroups: List[DimensionGroup] = []
    slicers: List[Slicer] = []


"""
Spreadsheets
"""


class DataSourceParameter(BaseModel):
    name: Optional[str]
    # UNION FIELDS
    namedRangeId: Optional[str]
    range: Optional[GoogleSheetsGridRange]
    # END UNION FIELDS

    @root_validator
    def only_one(cls, values):
        if len([v for k, v in values.items() if v and k in ["namedRangeId", "range"]]) == 1:
            return values

        raise ValueError("You must choose exactly one from range and namedRangeId.")


class DataSourceSpec(BaseModel):
    parameters: List[DataSourceParameter] = []
    bigQuery: Optional[Any]


class DataSource(BaseModel):
    sheetId: Optional[int]
    dataSourceId: Optional[str]
    spec: Optional[DataSourceSpec]
    calculatedColumns: List[DataSourceColumn] = []


class ThemeColorPair(BaseModel):
    colorType: Optional[ThemeColorType]
    color: Optional[GoogleColorStyle]


class SpreadsheetTheme(BaseModel):
    primaryFontFamily: str
    themeColors: List[ThemeColorPair] = []


class IterativeCalculationSettings(BaseModel):
    """
    Settings to control how circular dependencies are resolved with iterative calculation.
    """

    maxIterations: int
    convergenceThreshold: float


class SpreadsheetProperties(BaseModel):
    """
    Properties of a spreadsheet.
    """

    title: str
    locale: str
    autoRecalc: Optional[str]
    timeZone: Optional[str]
    defaultFormat: Optional[CellFormat]
    iterativeCalculationSettings: Optional[IterativeCalculationSettings]
    spreadsheetTheme: Optional[SpreadsheetTheme]


class Spreadsheet(BaseModel):
    """
    Represents the object returned from calling the spreadsheets.get() method
    """

    spreadsheetId: str
    properties: SpreadsheetProperties
    sheets: List[Sheet] = []
    namesRange: List[NamedRange] = []
    spreadsheetUrl: str
    developerMetadata: List[DeveloperMetadata] = []
    dataSources: List[DataSource] = []
    # dataSourceSchedules: List[DataSourceRefreshSchedule] = []
    dataSourceSchedules: List[Any] = []


class AddChartCommand(BaseModel):
    chart: GoogleSheetsChart


class AddChartsRequest(BaseModel):
    addChart: AddChartCommand
