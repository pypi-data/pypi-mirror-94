from py_gsuite_apis.services.google_apis.auth import (
    GoogleServerAuthCredentials,
    create_google_server_auth_services_credentials,
)
from py_gsuite_apis.services.google_apis.drive import GoogleDriveApiClient, create_google_drive_api_client
from py_gsuite_apis.services.google_apis.sheets import GoogleSheetsApiClient, create_google_sheets_api_client
from py_gsuite_apis.services.google_apis.slides import GoogleSlidesApiClient, create_google_slides_api_client

from py_gsuite_apis.models import google_apis as PyGsuiteModels

name = "py-gsuite-apis"

__version__ = "0.0.6"
__all__ = [
    "GoogleServerAuthCredentials",
    "create_google_server_auth_services_credentials",
    "GoogleDriveApiClient",
    "create_google_drive_api_client",
    "GoogleSheetsApiClient",
    "create_google_sheets_api_client",
    "GoogleSlidesApiClient",
    "create_google_slides_api_client",
    "PyGsuiteModels",
]
