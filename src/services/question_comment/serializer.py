"""serialzier file for question comment"""
from datetime import datetime
from typing import Optional, Any, List
from pydantic import BaseModel
from pydantic.types import constr, conint

from src.utils.common_serializer import SuccessResponsePartial


class QuestionCommentInbound(BaseModel):
    """class for save question inbound"""
    id: Optional[conint(gt=0)]
    question_id: conint(gt=0)
    is_internal: Optional[bool]
    body: constr(max_length=10000)
    parent_id: Optional[conint(gt=0)]


class QuestionCommentOutbound(BaseModel):
    """ class for question outbound"""
    id: int
    question_id: int
    parent_id: Optional[int]
    body: str
    is_internal: Optional[bool]
    created_by: Optional[Any]
    created_on: Optional[datetime]
    updated_by: Optional[Any]
    updated_on: Optional[datetime]
    meta_data: Optional[Any]


class QuestionCommentFinalOutBound(SuccessResponsePartial):
    """ response serializer for question comment"""
    data: Optional[List[QuestionCommentOutbound]]
