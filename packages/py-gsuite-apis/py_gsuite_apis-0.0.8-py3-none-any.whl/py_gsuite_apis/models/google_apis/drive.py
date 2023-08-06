from typing import Optional, List

from pydantic import BaseModel


class DriveCopyRequestBody(BaseModel):
    name: Optional[str]
    parents: List[str] = []
