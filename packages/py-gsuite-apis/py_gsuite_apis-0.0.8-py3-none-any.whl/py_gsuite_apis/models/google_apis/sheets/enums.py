# from typing import Literal
from typing_extensions import Literal

BooleanConditionType = Literal[
    "NUMBER_GREATER",
    "NUMBER_GREATER_THAN_EQ",
    "NUMBER_LESS",
    "NUMBER_LESS_THAN_EQ",
    "NUMBER_EQ",
    "NUMBER_NOT_EQ",
    "NUMBER_BETWEEN",
    "NUMBER_NOT_BETWEEN",
    "TEXT_CONTAINS",
    "TEXT_NOT_CONTAINS",
    "TEXT_STARTS_WITH",
    "TEXT_ENDS_WITH",
    "TEXT_EQ",
    "TEXT_IS_EMAIL",
    "TEXT_IS_URL",
    "DATE_EQ",
    "DATE_BEFORE",
    "DATE_AFTER",
    "DATE_ON_OR_BEFORE",
    "DATE_ON_OR_AFTER",
    "DATE_BETWEEN",
    "DATE_NOT_BETWEEN",
    "DATE_IS_VALID",
    "ONE_OF_RANGE",
    "ONE_OF_LIST",
    "BLANK",
    "NOT_BLANK",
    "CUSTOM_FORMULA",
    "BOOLEAN",
    "TEXT_NOT_EQ",
    "DATE_NOT_EQ",
]

RelativeDate = Literal[
    "PAST_YEAR",  # The value is one year before today.
    "PAST_MONTH",  # The value is one month before today.
    "PAST_WEEK",  # The value is one week before today.
    "YESTERDAY",  # The value is yesterday.
    "TODAY",  # The value is today.
    "TOMORROW",  # The value is tomorrow.
]
SortOrder = Literal["ASCENDING", "DESCENDING"]
SheetType = Literal[
    "GRID",  # The sheet is a grid.
    "OBJECT",  # The sheet has no grid and instead has an object like a chart or image.
    "DATA_SOURCE",  # The sheet connects with an external DataSource and shows the preview of data.
]
NumberFormatType = Literal[
    "TEXT", "NUMBER", "PERCENT", "CURRENCY", "DATE", "TIME", "DATE_TIME", "SCIENTIFIC",
]
BorderStyle = Literal[
    "DOTTED", "DASHED", "SOLID", "SOLID_MEDIUM", "SOLID_THICK", "NONE", "DOUBLE",
]
VerticalAlign = Literal["TOP", "MIDDLE", "BOTTOM"]
HorizontalAlign = Literal["LEFT", "CENTER", "RIGHT"]
WrapStrategy = Literal["OVERFLOW_CELL", "LEGACY_WRAP", "CLIP", "WRAP"]
TextDirection = Literal["LEFT_TO_RIGHT", "RIGHT_TO_LEFT"]
HyperlinkDisplayType = Literal["LINKED", "PLAIN_TEXT"]

ErrorType = Literal[
    "ERROR", "NULL_VALUE", "DIVIDE_BY_ZERO", "VALUE", "REF", "NAME", "NUM", "N_A", "LOADING",
]
DataExecutionState = Literal[
    "NOT_STARTED", "RUNNING", "SUCCEEDED", "FAILED",
]
DataExecutionErrorCode = Literal[
    "TIMED_OUT",
    "TOO_MANY_ROWS",
    "TOO_MANY_CELLS",
    "ENGINE",
    "PARAMETER_INVALID",
    "UNSUPPORTED_DATA_TYPE",
    "DUPLICATE_COLUMN_NAMES",
    "INTERRUPTED",
    "CONCURRENT_QUERY",
    "OTHER",
    "TOO_MANY_CHARS_PER_CELL",
    "DATA_NOT_FOUND",
    "PERMISSION_DENIED",
    "MISSING_COLUMN_ALIAS",
    "OBJECT_NOT_FOUND",
    "OBJECT_IN_ERROR_STATE",
    "OBJECT_SPEC_INVALID",
]

InterpolationPointType = Literal[
    "MIN", "MAX", "NUMBER", "PERCENT", "PERCENTILE",
]
ThemeColorType = Literal["TEXT", "BACKGROUND", "ACCENT1", "ACCENT2", "ACCENT3", "ACCENT4", "ACCENT5", "ACCENT6", "LINK"]
Dimension = Literal["ROWS", "COLUMNS"]
DataSourceTableColumnSelectionType = Literal["SELECTED", "SYNC_ALL"]
DeveloperMetadataVisibility = Literal["DOCUMENT", "PROJECT"]
DeveloperMetadataLocationType = Literal["ROW", "COLUMN", "SHEET", "SPREADSHEET"]
ChartHiddenDimensionStrategy = Literal[
    "SKIP_HIDDEN_ROWS_AND_COLUMNS", "SKIP_HIDDEN_ROWS", "SKIP_HIDDEN_COLUMNS", "SHOW_ALL",
]
