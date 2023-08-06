from typing import Optional

from pydantic import BaseModel

from py_gsuite_apis.models.google_apis.slides.enums import ArrowStyle, DashStyle, LineType, LineCategory
from py_gsuite_apis.models.google_apis.slides.other import HyperLink, SolidFill, Dimension


class LineFill(BaseModel):
    solidFill: Optional[SolidFill]


class LineConnection(BaseModel):
    connectedObjectId: Optional[str]
    connectionSiteIndex: Optional[int]


class LineProperties(BaseModel):
    """
    The properties of the Line .

    When unset, these fields default to values that match the appearance of new lines created in the Slides editor.
    """

    lineFill: Optional[LineFill]
    weight: Optional[Dimension]
    dashStyle: Optional[DashStyle]
    startArrow: Optional[ArrowStyle]
    endArrow: Optional[ArrowStyle]
    link: Optional[HyperLink]
    startConnection: Optional[LineConnection]
    endConnection: Optional[LineConnection]


class GoogleSlidesLine(BaseModel):
    """
    A PageElement kind representing a non-connector line, straight connector, curved connector, or bent connector.
    """

    lineProperties: Optional[LineProperties]
    lineType: Optional[LineType]
    lineCategory: Optional[LineCategory]
