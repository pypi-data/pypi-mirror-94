from typing import Optional

from pydantic import BaseModel

from py_gsuite_apis.models.google_apis.slides.other import ImageProperties


class GoogleSlidesImage(BaseModel):
    contentUrl: Optional[str]
    imageProperties: Optional[ImageProperties]
    sourceUrl: Optional[str]
