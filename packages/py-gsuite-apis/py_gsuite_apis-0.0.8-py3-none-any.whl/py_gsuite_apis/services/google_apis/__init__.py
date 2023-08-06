from typing import Union
import logging
from uuid import UUID, uuid4

from googleapiclient.discovery import build as DiscoveryBuild

from py_gsuite_apis.services.google_apis.auth import GoogleWebAuthCredentials, GoogleServerAuthCredentials


logger = logging.getLogger(__name__)


class GoogleApiClient(object):
    def __init__(
        self,
        *,
        credentials: Union[GoogleWebAuthCredentials, GoogleServerAuthCredentials],
        build: str = None,
        version: str = None,
        scope: str = None,
    ) -> None:
        self.creds = credentials.creds
        self.scope = scope
        self.build = build
        self.version = version

        logger.info(f"AUTHORIZED SERVICE FOR: {build} - {version} WITH SCOPE={scope}")
        self.service = DiscoveryBuild(build, version, credentials=self.creds)

    def create_object_id(self) -> UUID:
        return uuid4()
