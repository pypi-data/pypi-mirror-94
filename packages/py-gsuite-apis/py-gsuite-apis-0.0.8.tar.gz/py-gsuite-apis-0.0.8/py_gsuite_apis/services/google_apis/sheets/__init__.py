from typing import List

import pandas as pd
import logging
import string

from py_gsuite_apis.core.config import get_config
from py_gsuite_apis.services.google_apis import GoogleApiClient
from py_gsuite_apis.services.google_apis.auth import GoogleServerAuthCredentials
from py_gsuite_apis.services.google_apis.sheets.charts import GoogleSheetsChartGenerator

from py_gsuite_apis.models.google_apis.sheets import AddChartsRequest, Spreadsheet, Sheet
from py_gsuite_apis.models.google_apis.sheets.charts import BasicChartAxis


settings = get_config()

logger = logging.getLogger("uvicorn")


class GoogleSheetsApiClient(GoogleApiClient):
    def __init__(
        self,
        *,
        credentials: GoogleServerAuthCredentials,
        build: str,
        version: str,
        scope: str,
    ) -> None:
        super().__init__(
            credentials=credentials,
            build=build,
            version=version,
            scope=scope,
        )

    def get_spreadsheet_by_spreadsheet_id(self, *, spreadsheet_id: str) -> Spreadsheet:
        res = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

        if not res:
            raise ValueError("No spreadsheet found with that Id")

        spreadsheet = Spreadsheet(**res)

        return spreadsheet

    def get_sheet_for_spreadsheet_from_sheet_name(self, *, spreadsheet_id: str, sheet_name: str) -> Sheet:
        spreadsheet = self.get_spreadsheet_by_spreadsheet_id(spreadsheet_id=spreadsheet_id)

        return self.find_sheet_in_spreadsheet_by_sheet_name(spreadsheet=spreadsheet, sheet_name=sheet_name)

    def find_sheet_in_spreadsheet_by_sheet_name(self, *, spreadsheet: Spreadsheet, sheet_name: str) -> Sheet:
        matching_sheets = [sheet for sheet in spreadsheet.sheets if sheet.properties.title == sheet_name]

        if matching_sheets:
            return matching_sheets[0]

        raise ValueError("No sheet with that name was found on this spreadsheet.")

    def convert_col_num_to_alpha(self, col_num: int) -> str:
        """
        Takes column number like 10 and converts it to its alphabetical counterpart

        Ex.
            10 -> K
            0 -> A
            25 -> Z
            26 -> AA
            28 -> AC
        """
        alphabet = [c for c in string.ascii_uppercase]
        prefix_idx = col_num // 26
        prefix_alphabet = [""] + alphabet
        prefix = prefix_alphabet[prefix_idx]
        letter = alphabet[col_num]

        return prefix + letter

    def construct_sheet_range_string_from_numerical_row_and_column_position(
        self, *, row_start: int, row_end: int, col_start: int, col_end: int
    ) -> str:
        """
        Convert numerical cell positions for start and end into a range string like A1:H8
        """
        sheet_range_start = self.convert_col_num_to_alpha(col_start) + str(row_start)
        sheet_range_end = self.convert_col_num_to_alpha(col_end) + str(row_end)
        sheet_range = sheet_range_start + ":" + sheet_range_end

        return sheet_range

    def write_pandas_dataframe_to_sheet(
        self,
        *,
        df: pd.DataFrame,
        spreadsheet_id: str,
        sheet_name: str,
        sheet_range: str = "A1",
        remove_first_column_title: bool = False,
    ) -> None:
        """
        Uploads a pandas.dataframe to the desired page of a google sheets sheet.
        SERVICE ACCOUNT MUST HAVE PERMISIONS TO WRITE IN THE SHEET.
        Aditionally, pass a list with the new names of the columns.
        Data must be utf-8 encoded to avoid errors.
        """

        df.fillna(value="", inplace=True)
        cols = df.columns.tolist()
        if remove_first_column_title:
            cols[0] = ""
        rows = df.to_numpy().tolist()

        try:
            body = {
                "valueInputOption": "USER_ENTERED",
                "data": [{"range": sheet_name + "!" + sheet_range, "values": [cols] + rows}],
            }

            self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        except Exception as e:
            print(e)
            logger.warning(e)

    def construct_add_chart_request_for_spreadsheet_range(
        self,
        *,
        spreadsheet_id: str,
        sheet_name: str,
        chart_title: str,
        chart_id: str = None,
        chart_type: str = "COLUMN",
        chart_axes: List[BasicChartAxis] = [
            BasicChartAxis(position="LEFT_AXIS", title=None),
            BasicChartAxis(position="BOTTOM_AXIS", title=None),
        ],
        legend_position: str = "TOP_LEGEND",
        data_range_start_row_index: int = 0,
        data_range_end_row_index: int = None,
        data_range_start_col_index: int = 0,
        data_range_end_col_index: int = None,
    ) -> AddChartsRequest:
        """
        Create a chart for the provided data range in the appropriate Google Sheet.

        Only works if the first column is the domain
        """
        spreadsheet = None
        sheet = None

        try:
            spreadsheet = self.get_spreadsheet_by_spreadsheet_id(spreadsheet_id=spreadsheet_id)
        except Exception as e:
            logger.warning(e)
            raise ValueError("Spreadsheet with that ID could not located or accessed.")

        try:
            sheet = self.find_sheet_in_spreadsheet_by_sheet_name(spreadsheet=spreadsheet, sheet_name=sheet_name)
        except Exception as e:
            logger.warning(e)
            raise ValueError("Sheet with that name is not present in the provided spreadsheet.")

        chart_generator = GoogleSheetsChartGenerator(
            spreadsheet_id=spreadsheet.spreadsheetId,
            sheet_id=sheet.properties.sheetId,
            # anything else the chart generator might need
        )

        domains = [
            chart_generator.create_basic_chart_domain(
                # sheet_id=None,
                sheet_id=sheet.properties.sheetId,
                start_row_index=data_range_start_row_index,
                end_row_index=data_range_start_row_index + 1,
                start_column_index=data_range_start_col_index,
                end_column_index=data_range_end_col_index,
                # group_rule: ChartGroupRule = None,
                # aggregate_type: ChartAggregateType = None,
            )
        ]

        if not data_range_end_row_index:
            # default to last column in sheet if need be
            data_range_end_row_index = sheet.properties.gridProperties.columnCount

        series = [
            chart_generator.create_basic_chart_series(
                sheet_id=sheet.properties.sheetId,
                start_row_index=i,
                end_row_index=i + 1,
                start_column_index=data_range_start_col_index,
                end_column_index=data_range_end_col_index,
                # target_axis: BasicChartAxisPosition = "LEFT_AXIS",
                # basic_chart_type: BasicChartType = "COLUMN",
                # series_line_style: GoogleLineStyle = None,
                # series_data_label: DataLabel = None,
                # series_color: GoogleColor = None,
                # series_color_style: GoogleColorStyle = None,
                # series_point_style: GooglePointStyle = None,
                # series_style_overrides: BasicSeriesDataPointStyleOverride = None,
            )
            for i in range(data_range_start_row_index + 1, data_range_end_row_index)
        ]

        basic_chart_spec = chart_generator.create_basic_chart_spec(
            chart_type=chart_type,
            chart_axes=chart_axes,
            legend_position=legend_position,
            domains=domains,
            series=series,
            header_count=1,
        )

        chart_spec = chart_generator.create_google_sheets_chart_spec(
            title=chart_title,
            basic_charts_spec=basic_chart_spec,
            # need to think about other parameters here
        )

        add_chart_request = chart_generator.generate_add_chart_request(
            chart_id=chart_id,
            chart_spec=chart_spec,
            # could potentially use chart_position to add the charts to the actual sheet
            # right now it just defaults to new sheet
            # chart_position: GoogleSheetsEmbeddedObjectPosition = None,
            # chart_border: GoogleSheetsEmbeddedObjectBorder = None,
        )

        return add_chart_request

    def execute_add_charts_request(
        self,
        *,
        spreadsheet_id: str,
        list_of_add_chart_requests_to_execute: List[AddChartsRequest] = [],
    ) -> None:
        body = {
            "requests": [
                add_chart_request.dict(exclude_unset=True)
                for add_chart_request in list_of_add_chart_requests_to_execute
            ]
        }

        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body,
            ).execute()
        except Exception as e:
            print(e)
            logger.warning(e)


async def create_google_sheets_api_client(
    credentials: GoogleServerAuthCredentials,
    build: str = settings.SHEETS.BUILD,
    version: str = settings.SHEETS.VERSION,
    scope: str = settings.SHEETS.SCOPE,
) -> GoogleSheetsApiClient:
    return GoogleSheetsApiClient(credentials=credentials, build=build, version=version, scope=scope)
