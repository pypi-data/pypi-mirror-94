from typing import Optional

from pydantic import BaseModel

from py_gsuite_apis.models.google_apis.slides.enums import VideoSource
from py_gsuite_apis.models.google_apis.slides.other import Outline


class VideoProperties(BaseModel):
    """
    The properties of the Video.
    """

    outline: Optional[Outline]
    autoPlay: Optional[bool]
    start: Optional[int]
    end: Optional[int]
    mute: Optional[bool]


class GoogleSlidesVideo(BaseModel):
    id: Optional[str]
    url: Optional[str]
    source: Optional[VideoSource]
    videoProperties: Optional[VideoProperties]

