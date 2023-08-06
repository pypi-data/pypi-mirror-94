# from typing import Literal
from typing_extensions import Literal

BasicChartType = Literal[
    "BAR",  # A bar chart .
    "LINE",  # A line chart .
    "AREA",  # An area chart .
    "COLUMN",  # A column chart .
    "SCATTER",  # A scatter chart .
    "COMBO",  # A combo chart .
    "STEPPED_AREA",  # A stepped area chart .
]
BasicChartLegendPosition = Literal[
    "BOTTOM_LEGEND",  # The legend is rendered on the bottom of the chart.
    "LEFT_LEGEND",  # The legend is rendered on the left of the chart.
    "RIGHT_LEGEND",  # The legend is rendered on the right of the chart.
    "TOP_LEGEND",  # The legend is rendered on the top of the chart.
    "NO_LEGEND",  # No legend is rendered.
]
BasicChartAxisPosition = Literal[
    "BOTTOM_AXIS", "LEFT_AXIS", "RIGHT_AXIS",
]
BasicChartStackedType = Literal[
    "NOT_STACKED", "STACKED", "PERCENT_STACKED",
]
BasicChartCompareMode = Literal[
    "DATUM",  # Only the focused data element is highlighted and shown in the tooltip.
    "CATEGORY",  # All data elements with the same category (e.g., domain value) are shown in the tooltip.
]
ChartAggregateType = Literal[
    "AVERAGE",  # Average aggregate function.
    "COUNT",  # Count aggregate function.
    "MAX",  # Maximum aggregate function.
    "MEDIAN",  # Median aggregate function.
    "MIN",  # Minimum aggregate function.
    "SUM",  # Sum aggregate function.
]
DataLabelType = Literal[
    "NONE",
    "DATA",  # The data label is displayed using values from the series data.
    "CUSTOM",  # The data label is displayed using values from a custom data source indicated by customLabelData .
]
DataLabelPlacement = Literal[
    "CENTER",  # Center within a bar or column, both horizontally and vertically.
    "LEFT",  # To the left of a data point.
    "RIGHT",  # To the right of a data point.
    "ABOVE",  # Above a data point.
    "BELOW",  # Below a data point.
    "INSIDE_END",  # Inside a bar or column at the end (top if positive, bottom if negative).
    "INSIDE_BASE",  # Inside a bar or column at the base.
    "OUTSIDE_END",  # Outside a bar or column at the end.
]
PointShape = Literal[
    "CIRCLE",
    "DIAMOND",
    "HEXAGON",
    "PENTAGON",
    "SQUARE",
    "STAR",
    "TRIANGLE",
    # cool X marks the spot
    "X_MARK",
]
ViewWindowMode = Literal[
    # Follows the min and max exactly if specified.
    # If a value is unspecified, it will fall back to the PRETTY value.
    "EXPLICIT",
    "PRETTY",  # Chooses a min and max that make the chart look good. Both min and max are ignored in this mode.
]
LineDashType = Literal[
    "INVISIBLE",
    "CUSTOM",
    "SOLID",
    "DOTTED",
    "MEDIUM_DASHED",
    "MEDIUM_DASHED_DOTTED",
    "LONG_DASHED",
    "LONG_DASHED_DOTTED",
]
ChartDateTimeRuleType = Literal[
    "SECOND",
    "MINUTE",
    "HOUR",
    "HOUR_MINUTE",
    "HOUR_MINUTE_AMPM",
    "DAY_OF_WEEK",
    "DAY_OF_YEAR",
    "DAY_OF_MONTH",
    "DAY_MONTH",
    "MONTH",
    "QUARTER",
    "YEAR",
    "YEAR_MONTH",
    "YEAR_QUARTER",
    "YEAR_MONTH_DAY",
]
