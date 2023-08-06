from typing import Optional, List

from pydantic import BaseModel, conint, confloat, root_validator

from py_gsuite_apis.models.google_apis.sheets.enums import (
    BooleanConditionType,
    RelativeDate,
    SortOrder,
    HorizontalAlign,
    ErrorType,
    DataExecutionState,
    DataExecutionErrorCode,
    ThemeColorType,
)


class ErrorValue(BaseModel):
    type: Optional[ErrorType]
    message: Optional[str]


class ExtendedValue(BaseModel):
    numberValue: Optional[float]
    stringValue: Optional[str]
    boolValue: Optional[bool]
    formulaValue: Optional[str]
    errorValue: Optional[ErrorValue]


class DataExecutionStatus(BaseModel):
    state: Optional[DataExecutionState]
    errorCode: Optional[DataExecutionErrorCode]
    errorMessage: Optional[str]
    lastRefreshTime: Optional[str]


class BooleanConditionValue(BaseModel):
    """
    The value of the condition, exactly one must be set:
    either relativeDate or userEnteredValue

    A value the condition is based on.
    The value is parsed as if the user typed into a cell.

    Formulas are supported (and must begin with an = or a '+').
    """

    relativeDate: Optional[RelativeDate]
    userEnteredValue: Optional[str]

    @root_validator
    def only_one(cls, values):
        if len([v for v in values.values() if v]) == 1:
            return values

        raise ValueError("You must choose one from relativeDate and userEnteredValue - not both")


class BooleanCondition(BaseModel):
    """
    A condition that can evaluate to true or false.

    BooleanConditions are used by conditional formatting, data validation, and the criteria in filters.
    """

    type: BooleanConditionType
    values: List[BooleanConditionValue]


class GoogleColor(BaseModel):
    """ Representing Color values for Google colors - defaults to black """

    red: Optional[conint(ge=0, le=255)] = 0
    green: Optional[conint(ge=0, le=255)] = 0
    blue: Optional[conint(ge=0, le=255)] = 0
    alpha: Optional[confloat(ge=0, le=1)] = 1


class GoogleColorStyle(BaseModel):
    """Can only be one or the other"""

    rgbColor: Optional[GoogleColor]
    themeColor: Optional[ThemeColorType]

    @root_validator
    def only_one(cls, values):
        if len([v for v in values.values() if v]) == 1:
            return values

        raise ValueError("You must choose one from rgbColor and themeColor - not both")


class GoogleSheetsGridCoordinate(BaseModel):
    """
    A coordinate in a sheet. All indexes are zero-based.
    """

    sheetId: Optional[int]
    rowIndex: Optional[int]
    columnIndex: Optional[int]


class GoogleSheetsGridRange(BaseModel):
    """
    sheetId	- The sheet this range is on.
    startRowIndex - The start row (inclusive) of the range, or not set if unbounded.
    endRowIndex	- The end row (exclusive) of the range, or not set if unbounded.
    startColumnIndex	- The start column (inclusive) of the range, or not set if unbounded.
    endColumnIndex	- The end column (exclusive) of the range, or not set if unbounded.
    """

    sheetId: Optional[int]
    startRowIndex: Optional[int]
    endRowIndex: Optional[int]
    startColumnIndex: Optional[int]
    endColumnIndex: Optional[int]


class GoogleSheetsTextFormat(BaseModel):
    foregroundColor: Optional[GoogleColor]
    foregroundColorStyle: Optional[GoogleColorStyle]
    fontFamily: Optional[str]
    fontSize: Optional[int]
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False


class GoogleSheetsTextPosition(BaseModel):
    horizontalAlignment: HorizontalAlign = "LEFT"


class GoogleSheetsFilterCriteria(BaseModel):
    hiddenValues: List[str] = []
    condition: Optional[BooleanCondition]
    visibleBackgroundColor: Optional[GoogleColor]
    visibleBackgroundColorStyle: Optional[GoogleColorStyle]
    visibleForegroundColor: Optional[GoogleColor]
    visibleForegroundColorStyle: Optional[GoogleColorStyle]


class GoogleSheetsFilterSpec(BaseModel):
    filterCriteria: Optional[GoogleSheetsFilterCriteria]
    # UNION FIELDS
    columnIndex: Optional[int]
    # dataSourceColumnReference: Optional[DataSourceColumnReference]
    # END OF UNION FIELDS


class GoogleSheetsSortSpec(BaseModel):
    """
    A sort order associated with a specific column or row.
    """

    sortOrder: Optional[SortOrder]
    foregroundColor: Optional[GoogleColor]
    foregroundColorStyle: Optional[GoogleColorStyle]
    backgroundColor: Optional[GoogleColor]
    backgroundColorStyle: Optional[GoogleColorStyle]
    #  UNION FIELDS
    dimensionIndex: Optional[int]
    # dataSourceColumnReference: Optional[DataSourceColumnReference]
    # END OF UNION FIELDS


class GoogleSheetsOverlayPosition(BaseModel):
    """
    The location an object is overlaid on top of a grid.
    """

    anchorCell: Optional[GoogleSheetsGridCoordinate]
    offsetXPixels: Optional[int]
    offsetYPixels: Optional[int]
    widthPixels: Optional[int]
    heightPixels: Optional[int]


class GoogleSheetsEmbeddedObjectPosition(BaseModel):
    """
    If newSheet is true, the embedded object is put on a new sheet whose ID is chosen for you. Used only when writing.
    """

    sheetId: Optional[int]
    overlayPosition: Optional[GoogleSheetsOverlayPosition]
    newSheet: Optional[bool]

    @root_validator
    def only_one(cls, values):
        if len([v for v in values.values() if v]) == 1:
            return values

        raise ValueError("You must choose only one from sheetId, overlayPosition, and newSheet.")


class DataSourceColumnReference(BaseModel):
    """
    An unique identifier that references a data source column.
    """

    name: str


class DataSourceColumn(BaseModel):
    reference: Optional[DataSourceColumnReference]
    formula: Optional[str]
