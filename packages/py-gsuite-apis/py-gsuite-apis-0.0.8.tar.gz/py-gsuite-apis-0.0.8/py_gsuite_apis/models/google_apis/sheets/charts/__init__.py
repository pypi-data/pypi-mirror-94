from typing import Optional, List, Union

from pydantic import BaseModel, validator, ValidationError

from py_gsuite_apis.models.google_apis.sheets.other import (
    DataSourceColumnReference,
    GoogleColor,
    GoogleColorStyle,
    GoogleSheetsGridRange,
    GoogleSheetsTextFormat,
    GoogleSheetsTextPosition,
    GoogleSheetsFilterSpec,
    GoogleSheetsSortSpec,
    GoogleSheetsEmbeddedObjectPosition,
)
from py_gsuite_apis.models.google_apis.sheets.enums import ChartHiddenDimensionStrategy
from py_gsuite_apis.models.google_apis.sheets.charts.enums import (
    BasicChartType,
    BasicChartLegendPosition,
    BasicChartAxisPosition,
    BasicChartCompareMode,
    BasicChartStackedType,
    ChartAggregateType,
    ChartDateTimeRuleType,
    DataLabelType,
    DataLabelPlacement,
    LineDashType,
    PointShape,
    ViewWindowMode,
    # ChartHiddenDimensionStrategy,
)


class GoogleSheetsDataSourceChartProperties(BaseModel):
    dataSourceId: Optional[str]
    dataExecutionStatus: Optional[dict]


class ChartSourceRange(BaseModel):
    sources: List[GoogleSheetsGridRange] = []


class ChartDateTimeRule(BaseModel):
    type: Optional[ChartDateTimeRuleType]


class ChartHistogramRule(BaseModel):
    """
    Allows you to organize numeric values in a source data column into
    buckets of constant size.
    """

    minValue: Optional[float]
    maxValue: Optional[float]
    intervalSize: Optional[float]


class ChartGroupRule(BaseModel):
    # one or the other!
    dateTimeRule: Optional[ChartDateTimeRule]
    histogramRule: Optional[ChartHistogramRule]


class ChartData(BaseModel):
    """
    The data included in a domain or series.
    """

    groupRule: Optional[ChartGroupRule]
    aggregateType: Optional[ChartAggregateType]


class SourceRangeChartData(ChartData):
    sourceRange: Optional[ChartSourceRange]


class ColumnReferenceChartData(ChartData):
    columnReference: Optional[DataSourceColumnReference]


class DataLabel(BaseModel):
    """
    Settings for one set of data labels.

    Data labels are annotations that appear next to a set of data,
    such as the points on a line chart, and provide additional information
    about what the data represents, such as a text representation of the value
    behind that point on the graph.
    """

    type: Optional[DataLabelType]
    textFormat: Optional[GoogleSheetsTextFormat]
    placement: Optional[DataLabelPlacement]
    # only used if type is set to custom
    customLabelData: Optional[ChartData]

    @validator("customLabelData", pre=True, always=True)
    def custom_label_data_only_with_custom(cls, v, values):
        if v and values["type"] == "CUSTOM":
            return v

        raise ValidationError("Custom label data only goes with a custom data label type")


class GoogleLineStyle(BaseModel):
    """
    Properties that describe the style of a line.
    """

    width: Optional[int]
    type: Optional[LineDashType]


class GooglePointStyle(BaseModel):
    size: Optional[int]
    shape: Optional[PointShape]


class BasicSeriesDataPointStyleOverride(BaseModel):
    index: Optional[int]
    color: Optional[GoogleColor]
    colorStyle: Optional[GoogleColorStyle]
    pointStyle: Optional[GooglePointStyle]


class GoogleChartAxisViewWindowOptions(BaseModel):
    """
    The options that define a "view window" for a chart
    (such as the visible values in an axis).
    """

    viewWindowMin: Optional[float]
    viewWindowMax: Optional[float]
    viewWindowMode: Optional[ViewWindowMode] = "PRETTY"


class BasicChartAxis(BaseModel):
    """
    An axis of the chart.

    A chart may not have more than one axis per axis position .
    """

    title: Optional[str]
    format: Optional[GoogleSheetsTextFormat]
    titleTextPosition: Optional[GoogleSheetsTextPosition]
    viewWindowOptions: Optional[GoogleChartAxisViewWindowOptions]
    position: Optional[BasicChartAxisPosition]


class BasicChartDomain(BaseModel):
    """
    The domain of a chart. For example, =
    if charting stock prices over time, this would be the date.
    """

    # domain: Optional[ChartData]
    domain: Union[SourceRangeChartData, ColumnReferenceChartData]
    # domain: SourceRangeChartData
    reversed: bool = False


class BasicChartSeries(BaseModel):
    """
    A single series of data in a chart.

    For example, if charting stock prices over time, multiple series may exist,
    one for the "Open Price", "High Price", "Low Price" and "Close Price".

    """

    series: Optional[ChartData]
    targetAxis: Optional[BasicChartAxisPosition]
    type: Optional[BasicChartType]
    lineStyle: Optional[GoogleLineStyle]
    dataLabel: Optional[DataLabel]
    color: Optional[GoogleColor]
    colorStyle: Optional[GoogleColorStyle]
    pointStyle: Optional[GooglePointStyle]
    styleOverrides: Optional[BasicSeriesDataPointStyleOverride]


class BasicChartSpec(BaseModel):
    """
    The specification for a basic chart.
    """

    chartType: BasicChartType
    legendPosition: BasicChartLegendPosition
    axis: List[BasicChartAxis] = []  # The axis on the chart.
    domains: List[BasicChartDomain] = []  # The domain of data this is charting. Only a single domain is supported.
    series: List[BasicChartSeries] = []  # The data this chart is visualizing.

    # The number of rows or columns in the data that are "headers".
    # If not set, Google Sheets will guess how many rows are headers based on the data.
    headerCount: Optional[int]

    threeDimensional: bool = False
    interpolateNulls: bool = False
    lineSmoothing: bool = False
    stackedType: Optional[BasicChartStackedType] = "NOT_STACKED"
    compareMode: Optional[BasicChartCompareMode]
    totalDataLabel: Optional[DataLabel]


class GoogleSheetsChartSpec(BaseModel):
    """
    The specifications of a chart
    """

    title: Optional[str]
    alText: Optional[str]
    titleTextFormat: Optional[GoogleSheetsTextFormat]
    titleTextPosition: Optional[GoogleSheetsTextPosition]

    subtitle: Optional[str]
    subtitleTextFormat: Optional[GoogleSheetsTextFormat]
    subtitleTextPosition: Optional[GoogleSheetsTextPosition]

    fontName: Optional[str]
    maximized: Optional[bool]

    backgroundColor: Optional[GoogleColor]
    backgroundColorStyle: Optional[GoogleColorStyle]

    dataSourceChartProperties: Optional[GoogleSheetsDataSourceChartProperties]
    filterSpecs: List[GoogleSheetsFilterSpec] = []
    sortSpecs: List[GoogleSheetsSortSpec] = []

    hiddenDimensionStrategy: Optional[ChartHiddenDimensionStrategy]


class GoogleSheetsChartSpecBasic(GoogleSheetsChartSpec):
    basicChart: BasicChartSpec


class GoogleSheetsChartSpecPie(GoogleSheetsChartSpec):
    pieChart: dict


class GoogleSheetsChartSpecBubble(GoogleSheetsChartSpec):
    bubbleChart: dict


class GoogleSheetsChartSpecCandlestick(GoogleSheetsChartSpec):
    candlestickChart: dict


class GoogleSheetsChartSpecOrg(GoogleSheetsChartSpec):
    orgChart: dict


class GoogleSheetsChartSpecHistogram(GoogleSheetsChartSpec):
    histogramChart: dict


class GoogleSheetsChartSpecWaterfall(GoogleSheetsChartSpec):
    waterfallChart: dict


class GoogleSheetsChartSpecTreemap(GoogleSheetsChartSpec):
    treemapChart: dict


class GoogleSheetsChartSpecScorecard(GoogleSheetsChartSpec):
    scorecardChart: dict


class GoogleSheetsEmbeddedObjectBorder(BaseModel):
    color: Optional[GoogleColor]
    colorStyle: Optional[GoogleColorStyle]


class GoogleSheetsChart(BaseModel):
    chartId: Optional[int]
    spec: Optional[GoogleSheetsChartSpec]
    position: Optional[GoogleSheetsEmbeddedObjectPosition]
    # position: GoogleSheetsEmbeddedObjectPosition
    border: Optional[GoogleSheetsEmbeddedObjectBorder]

    @validator("position", pre=True, always=True)
    def default_position(cls, v, values):
        """Default position to a new sheet"""
        return v or GoogleSheetsEmbeddedObjectPosition(newSheet=True)
