from typing import List

import logging

from py_gsuite_apis.core.config import get_config

from py_gsuite_apis.services.google_apis import GoogleApiClient
from py_gsuite_apis.services.google_apis.auth import GoogleServerAuthCredentials

from py_gsuite_apis.models.google_apis.drive import DriveCopyRequestBody


settings = get_config()

logger = logging.getLogger("uvicorn")


class GoogleDriveApiClient(GoogleApiClient):
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

    def create_slides_presentation_copy(
        self,
        *,
        slides_presentation_id: str,
        copy_title: str,
        parents: List[str] = None,
    ) -> str:
        """
        Creates a copy of the given slides presentation in Google Drive and returns the copied
        slide deck ID
        """
        drive_copy_request_body = DriveCopyRequestBody(name=copy_title, parents=parents or [])
        drive_response = (
            self.service.files()
            .copy(fileId=slides_presentation_id, body=drive_copy_request_body.dict(exclude_unset=True))
            .execute()
        )
        slides_presentation_copy_id = drive_response.get("id")
        return slides_presentation_copy_id


async def create_google_drive_api_client(
    credentials: GoogleServerAuthCredentials,
    build: str = settings.DRIVE.BUILD,
    version: str = settings.DRIVE.VERSION,
    scope: str = settings.DRIVE.SCOPE,
) -> GoogleDriveApiClient:
    return GoogleDriveApiClient(credentials=credentials, build=build, version=version, scope=scope)
