"""serializer file for question"""
from datetime import date
from typing import Optional, List, Any

from pydantic import BaseModel
from pydantic.types import conint
from src.utils.common_serializer import SuccessResponsePartial


class LogsInBound(BaseModel):
    """serializer for question"""
    id: Optional[conint(gt=0)]
    question_id: Optional[conint(gt=0)]
    previous_question: Optional[str]
    next_question: Optional[str]


class LogsOutBound(BaseModel):
    """outbound for question"""
    id: Optional[conint(gt=0)]
    question_id: Optional[conint(gt=0)]
    previous_question: Optional[str]
    next_question: Optional[str]
    created_by: Optional[Any]
    created_on: Optional[date]


class LogsGetOutBound(SuccessResponsePartial):
    """save and update response"""
    data: Optional[List[LogsOutBound]]

