from typing import List, Optional

from pydantic import BaseModel


class JobBoardList(BaseModel):
    title: str
    description: Optional[str] = None