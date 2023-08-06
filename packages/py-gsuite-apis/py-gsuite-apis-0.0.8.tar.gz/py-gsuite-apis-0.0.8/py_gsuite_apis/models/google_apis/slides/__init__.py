from typing import Optional, List

from pydantic import BaseModel

from py_gsuite_apis.models.google_apis.slides.page import GoogleSlidesPage
from py_gsuite_apis.models.google_apis.slides.other import Size


"""
Presentations
"""


class GoogleSlidesPresentation(BaseModel):
    presentationId: Optional[str]
    title: Optional[str]
    locale: Optional[str]
    revisisonId: Optional[str]
    pageSize: Optional[Size]
    slides: List[GoogleSlidesPage] = []
    masters: List[GoogleSlidesPage] = []
    layouts: List[GoogleSlidesPage] = []
    notesMaster: Optional[GoogleSlidesPage]
