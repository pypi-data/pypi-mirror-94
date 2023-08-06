from abc import ABC, abstractmethod
from typing import Any

import os
import logging

from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from py_gsuite_apis.core.config import get_config
from py_gsuite_apis.services import fs_conn


settings = get_config()

logger = logging.getLogger("uvicorn")


class GoogleAuthCredentials(ABC):
    def __init__(
        self, *, credentials_filename: str = None, credentials_filepath: str = None, scope: str = None
    ) -> None:
        self.creds = self.fetch_credentials(
            credentials_filename=credentials_filename, credentials_filepath=credentials_filepath, scope=scope
        )

    @abstractmethod
    def fetch_credentials(
        self, *, credentials_filename: str = None, credentials_filepath: str = None, scope: str = None
    ) -> Any:
        raise NotImplementedError


class GoogleAuthCredentialsBase(GoogleAuthCredentials):
    def get_service_account_credentials_path(
        self, *, credentials_filename: str = None, credentials_filepath: str = None
    ) -> str:
        if not credentials_filename and not credentials_filepath:
            logger.warning(
                f"Credentials filename: {credentials_filename} - Credentials filepath: {credentials_filepath}"
            )
            raise ValueError("Must include either a valid credentials filename or valid credentials filepath.")

        service_credentials_path = None

        if credentials_filename and os.path.isfile(
            os.path.join(os.path.expanduser("~"), ".credentials", credentials_filename)
        ):
            service_credentials_path = os.path.join(os.path.expanduser("~"), ".credentials", credentials_filename)
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        if credentials_filename and os.path.isfile(os.path.join(".credentials", credentials_filename)):
            service_credentials_path = os.path.join(".credentials", credentials_filename)
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        if credentials_filename and fs_conn.is_file(filepath=credentials_filename):
            service_credentials_path = fs_conn.get_file_path(filepath=credentials_filename)
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        if credentials_filepath and fs_conn.is_file(filepath=credentials_filepath):
            service_credentials_path = fs_conn.get_file_path(filepath=credentials_filepath)
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        if credentials_filename and os.path.isfile(f"./{credentials_filename}"):
            service_credentials_path = f"./{credentials_filename}"
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        if credentials_filepath and os.path.isfile(f"./{credentials_filepath}"):
            service_credentials_path = f"./{credentials_filepath}"
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        if credentials_filename and os.path.isfile(os.path.join(os.path.expanduser("~"), credentials_filename)):
            service_credentials_path = os.path.join(os.path.expanduser("~"), credentials_filename)
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        if credentials_filepath and os.path.isfile(os.path.join(os.path.expanduser("~"), credentials_filepath)):
            service_credentials_path = os.path.join(os.path.expanduser("~"), credentials_filepath)
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        logger.warning(
            f"Invalid credentials arguments: Credentials filename: {credentials_filename}"
            f" - Credentials filepath: {os.path.abspath(credentials_filepath)}"
            f" - Credentials filepath: {os.path.abspath(os.path.join(os.path.expanduser('~'), credentials_filepath))}"
        )
        raise Exception("UNABLE TO FIND CREDENTIALS FILE | Check the instructions in the setup_credentials.md file")


class GoogleWebAuthCredentials(GoogleAuthCredentialsBase):
    def fetch_credentials(
        self, *, credentials_filename: str = None, credentials_filepath: str = None, scope: str = None
    ) -> Any:
        creds = fs_conn.fetch_google_oauth_token()

        SERVICE_ACCOUNT_CREDENTIALS_FILEPATH = self.get_service_account_credentials_path(
            credentials_filename=credentials_filename,
            credentials_filepath=credentials_filepath,
        )

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    SERVICE_ACCOUNT_CREDENTIALS_FILEPATH,
                    scope,
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            fs_conn.save_google_oauth_credentials_to_pickle_file(creds)

        return creds


class GoogleServerAuthCredentials(GoogleAuthCredentialsBase):
    def fetch_credentials(
        self, *, credentials_filename: str = None, credentials_filepath: str = None, scope: str = None
    ) -> Any:
        SERVICE_ACCOUNT_SCOPES = [
            "https://www.googleapis.com/auth/sqlservice.admin",
            settings.SLIDES.SCOPE,
            settings.SHEETS.SCOPE,
            settings.DRIVE.SCOPE,
            "https://www.googleapis.com/auth/drive.file",
        ]

        SERVICE_ACCOUNT_CREDENTIALS_FILEPATH = self.get_service_account_credentials_path(
            credentials_filename=credentials_filename,
            credentials_filepath=credentials_filepath,
        )

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_CREDENTIALS_FILEPATH, scopes=SERVICE_ACCOUNT_SCOPES
        )

        return credentials


async def create_google_server_auth_services_credentials(
    credentials_filename: str = "google-service-account-credentials.json",
    credentials_filepath: str = None,
) -> GoogleServerAuthCredentials:
    return GoogleServerAuthCredentials(
        credentials_filename=credentials_filename, credentials_filepath=credentials_filepath
    )
