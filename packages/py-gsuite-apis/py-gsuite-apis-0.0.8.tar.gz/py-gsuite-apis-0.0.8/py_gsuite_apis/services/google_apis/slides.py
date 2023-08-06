from typing import List, Union

import logging

from py_gsuite_apis.core.config import get_config

from py_gsuite_apis.services.google_apis import GoogleApiClient
from py_gsuite_apis.services.google_apis.auth import GoogleServerAuthCredentials
from py_gsuite_apis.models.google_apis.slides import GoogleSlidesPresentation
from py_gsuite_apis.models.google_apis.slides.requests import (
    CreateTableRequest,
    CreateTableRequestBody,
    CreateShapeRequest,
    CreateSlideRequest,
    DeleteSlideRequest,
    PageElementProperties,
    SubstringMatchCriteria,
    CreateSheetsChartRequest,
    CreateSheetsChartRequestBody,
    InsertTextIntoTableRequest,
    InsertTextRequestBody,
    InsertTableRowsRequest,
    InsertTableRowsRequestBody,
    InsertTableColumnsRequest,
    InsertTableColumnsRequestBody,
    ReplaceAllTextRequest,
    ReplaceAllTextRequestBody,
    ReplaceAllShapesWithSheetsChartRequest,
    ReplaceAllShapesWithSheetsChartRequestBody,
)
from py_gsuite_apis.models.google_apis.slides.other import Size, AffineTransform
from py_gsuite_apis.models.google_apis.slides.enums import LinkingMode
from py_gsuite_apis.models.google_apis.slides.table import TableCellLocation
from py_gsuite_apis.models.google_apis.slides.page import GoogleSlidesPage


settings = get_config()

logger = logging.getLogger("uvicorn")


BatchUpdateRequest = Union[
    CreateSheetsChartRequest,
    Union[
        CreateTableRequest,
        Union[
            ReplaceAllShapesWithSheetsChartRequest,
            Union[
                InsertTextIntoTableRequest,
                Union[
                    CreateShapeRequest,
                    CreateSlideRequest,
                ],
            ],
        ],
    ],
]


class GoogleSlidesApiClient(GoogleApiClient):
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

    def execute_batch_update(self, *, requests: List[BatchUpdateRequest], presentation_id: str) -> None:
        """Executes a batch update request for a presentation"""
        try:
            body = {"requests": [r.dict(exclude_unset=True) for r in requests]}

            self.service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
        except Exception as e:
            logger.warning(e)
            raise e

    def get_presentation_by_id(self, *, presentation_id: str) -> GoogleSlidesPresentation:
        """Gets a presentation object by id"""
        try:
            presentation = self.service.presentations().get(presentationId=presentation_id).execute()
            if not presentation:
                raise ValueError("Presentation with that ID could not located or accessed.")

            return GoogleSlidesPresentation(**presentation)
        except Exception as e:
            logger.warning(e)
            raise ValueError("Presentation with that ID could not located or accessed.") from e

    def get_presentation_slides_by_presentation_id(self, *, presentation_id: str) -> List[GoogleSlidesPage]:
        """Gets all the slides present on a given presentation object"""
        presentation = self.get_presentation_by_id(presentation_id=presentation_id)

        return presentation.slides

    def get_last_slides_page_of_presentation(self, *, presentation_id: str) -> GoogleSlidesPage:
        slides = self.get_presentation_slides_by_presentation_id(presentation_id=presentation_id)

        return slides[-1]

    def get_table_element_in_presentation_slide(self, *, slide: GoogleSlidesPage) -> str:
        """
        Returns the first table element found in the slide
        """
        for element in slide.pageElements:
            if getattr(element, "table", None):
                return element

    def construct_delete_last_slide_of_presentation_request(self, *, presentation_id: str) -> DeleteSlideRequest:
        last_slide = self.get_last_slides_page_of_presentation(presentation_id=presentation_id)
        return self.construct_delete_slide_request(slide_id=last_slide.objectId)

    def construct_delete_slide_request(self, *, slide_id: str) -> DeleteSlideRequest:
        """
        Given the object id of a slide, create a request to delete it
        """
        return DeleteSlideRequest(objectId=slide_id)

    def construct_create_table_request(
        self,
        *,
        table_object_id: str = None,
        num_rows: int = 1,
        num_columns: int = 1,
        page_object_id: str = None,
        # API ignores the size and affine
        # element_size: Size = None,
        # element_affine_transform: AffineTransform = None,
    ) -> CreateTableRequest:
        """
        Creates a new table on a Google Slide

        Slides API is stupid and ignores the element size and transformation provided.

        It instead just centers it on the slide and then makes it big enough to accommodate all rows and cols. Dumb.

        Taken from: https://developers.google.com/slides/samples/tables

        A better idea might be to start with a tiny table and just transform it until it matches our needs.
        """
        element_properties = (
            PageElementProperties(
                pageObjectId=page_object_id,  # The object ID of the page where the element is located.
                # size=element_size,
                # transform=element_affine_transform,
            )
            if page_object_id is not None
            else None
        )

        return CreateTableRequest(
            createTable=CreateTableRequestBody(
                objectId=table_object_id,
                elementProperties=element_properties,
                rows=num_rows,
                columns=num_columns,
            )
        )

    def construct_add_columns_to_table_request(
        self,
        *,
        table_object_id: str,
        insert_right: bool = True,
        number_of_columns_to_insert: int,
        table_cell_row_index: int,
        table_cell_col_index: int,
    ) -> InsertTableColumnsRequest:
        """
        Adds columns to a table object on a Google Slide
        """
        return InsertTableColumnsRequest(
            insertTableColumns=InsertTableColumnsRequestBody(
                tableObjectId=table_object_id,
                cellLocation=TableCellLocation(
                    rowIndex=table_cell_row_index,  # zero indexed
                    columnIndex=table_cell_col_index,  # zero indexed
                ),
                insertRight=insert_right,
                number=number_of_columns_to_insert,
            )
        )

    def construct_add_rows_to_table_request(
        self,
        *,
        table_object_id: str,
        insert_below: bool = True,
        number_of_rows_to_insert: int,
        table_cell_row_index: int,
        table_cell_col_index: int,
    ) -> InsertTableRowsRequest:
        """
        Adds rows to a table object on a Google Slide
        """
        return InsertTableRowsRequest(
            insertTableRows=InsertTableRowsRequestBody(
                tableObjectId=table_object_id,
                cellLocation=TableCellLocation(
                    rowIndex=table_cell_row_index,  # zero indexed
                    columnIndex=table_cell_col_index,  # zero indexed
                ),
                insertBelow=insert_below,
                number=number_of_rows_to_insert,
            )
        )

    def construct_create_sheets_chart_request(
        self,
        *,
        new_sheets_chart_object_id: str = None,
        spreadsheet_id: str,
        chart_id: str,
        chart_linking_mode: str = "NOT_LINKED_IMAGE",
        page_object_id: str,
        element_size: Size = None,
        element_affine_transform: AffineTransform = None,
    ) -> CreateSheetsChartRequest:
        """
        Creates a new chart in a Google Slide from a chart existing in a Google Sheet
        """
        return CreateSheetsChartRequest(
            createSheetsChart=CreateSheetsChartRequestBody(
                objectId=new_sheets_chart_object_id,
                elementProperties=PageElementProperties(
                    pageObjectId=page_object_id,  # The object ID of the page where the element is located.
                    size=element_size,
                    transform=element_affine_transform,
                ),
                spreadsheetId=spreadsheet_id,
                chartId=chart_id,
                linkingMode=chart_linking_mode,
            )
        )

    def construct_replace_all_text_request(
        self,
        *,
        text_pattern_to_replace: str,
        match_case: bool = False,
        new_text: str,
    ) -> ReplaceAllTextRequest:
        return ReplaceAllTextRequest(
            replaceAllText=ReplaceAllTextRequestBody(
                containsText=SubstringMatchCriteria(
                    text=text_pattern_to_replace,
                    matchCase=match_case,  # whether or not to have match be case sensitive
                ),
                replaceText=new_text,
            )
        )

    def construct_replace_all_shapes_with_sheets_chart_request(
        self,
        *,
        spreadsheet_id: str,
        chart_id: str,
        text_to_match: str,
        matching_is_case_sensitive: bool = False,
        linking_mode: LinkingMode = "NOT_LINKED_IMAGE",
        page_object_ids: List[str] = [],
    ) -> ReplaceAllShapesWithSheetsChartRequest:
        """
        Will find shapes on a Google Slide that match a certain pattern, and replace them with shapes
        """
        return ReplaceAllShapesWithSheetsChartRequest(
            replaceAllShapesWithSheetsChart=ReplaceAllShapesWithSheetsChartRequestBody(
                chartId=chart_id,
                spreadsheetId=spreadsheet_id,
                containsText=SubstringMatchCriteria(
                    text=text_to_match,
                    matchCase=matching_is_case_sensitive,
                ),
                linkingMode=linking_mode,
                pageObjectIds=page_object_ids,
            )
        )

    def construct_insert_text_into_table_request(
        self,
        *,
        table_object_id: str,
        table_cell_row_index: int,  # zero-indexed
        table_cell_col_index: int,  # zero-indexed
        text_to_insert: str,
        insertion_index: int = 0,
    ) -> InsertTextIntoTableRequest:
        return InsertTextIntoTableRequest(
            insertText=InsertTextRequestBody(
                objectId=table_object_id,
                cellLocation=TableCellLocation(
                    rowIndex=table_cell_row_index,
                    columnIndex=table_cell_col_index,
                ),
                text=text_to_insert,
                insertionIndex=insertion_index,
            )
        )


async def create_google_slides_api_client(
    credentials: GoogleServerAuthCredentials,
    build: str = settings.SLIDES.BUILD,
    version: str = settings.SLIDES.VERSION,
    scope: str = settings.SLIDES.SCOPE,
) -> GoogleSlidesApiClient:
    return GoogleSlidesApiClient(credentials=credentials, build=build, version=version, scope=scope)
