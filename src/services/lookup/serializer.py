"""serializer file for lookup """
from enum import Enum
from typing import Optional, Any, List

from pydantic import BaseModel

from src.services.master.question.serializer import AreaSingleOutbound, CourseSingleOutbound


class Model(str, Enum):
    """Models"""
    QUESTION               = "question"
    AREA                   = "area"
    COURSE                 = "course"


class LookupOutBound(BaseModel):
    """lookup outbound"""
    question: Optional[Any]
    area: Optional[List[AreaSingleOutbound]]
    course: Optional[List[CourseSingleOutbound]]
