"""serializer file for question"""
from datetime import date
from typing import Optional, Dict, List, Text, Any

from pydantic import BaseModel
from pydantic.types import conint, conlist, constr

from src.configs.constants import QuestionConstant
from src.configs.lookup_constant import QUESTION
from src.utils.common_serializer import SuccessResponsePartial


class QuestionInbound(BaseModel):
    """serializer for question"""
    id: Optional[conint(gt=0)]
    org_id: Optional[conint(gt=0)]
    is_public: Optional[bool]
    area_ids: conlist(item_type=int, unique_items=True)
    lod: Optional[int]
    question_style: Optional[conint(gt=0, le=max(QUESTION.get("question_style").keys()))] = QuestionConstant.QuestionStyle.SINGLE_SCREEN
    no_of_option: Optional[conint(gt=0, le=max(QUESTION.get("number_of_option").keys()))]
    marking_range: Optional[int]
    typable_text_type: Optional[int]
    direction_id: Optional[int]
    course_ids: Optional[conlist(item_type=int, unique_items=True)]
    question_type: conint(gt=0, le=max(QUESTION.get("question_type").keys()))
    answer_type: Optional[int]
    answer: Optional[conlist(item_type=int, unique_items=True)]
    editor: Optional[int]
    typable_answer: Optional[str]
    question: str
    explanation: Optional[str]
    option1: Optional[str]
    option2: Optional[str]
    option3: Optional[str]
    option4: Optional[str]
    option5: Optional[str]
    option6: Optional[str]
    tags: Optional[List[constr(max_length=200)]]


class QuestionOutBound(BaseModel):
    """outbound for question"""
    id: Optional[conint(gt=0)]
    org_id: Optional[conint(gt=0)]
    is_public: Optional[bool]
    area_ids: Optional[List[int]]
    lod: Optional[int]
    question_style: Optional[int]
    no_of_option: Optional[int]
    marking_range: Optional[int]
    typable_text_type: Optional[int]
    direction_id: Optional[int]
    course_ids: Optional[List[int]]
    question_type: Optional[int]
    answer_type: Optional[int]
    answer: Optional[List[int]]
    editor: Optional[int]
    typable_answer: Optional[str]
    question: str
    explanation: Optional[str]
    option1: Optional[str]
    option2: Optional[str]
    option3: Optional[str]
    option4: Optional[str]
    option5: Optional[str]
    option6: Optional[str]
    created_by: Optional[Any]
    created_on: Optional[date]
    updated_by: Optional[Any]
    updated_on: Optional[date]
    meta_data: Optional[Dict]
    tags: Optional[List[str]]


class QuestionGetOutBound(SuccessResponsePartial):
    """save and update response"""
    data: Optional[QuestionOutBound]


class QuestionAllFilterInbound(BaseModel):
    """filter inbound"""
    org_id: Optional[List[conint(strict=True, gt=0)]]
    question_style: Optional[List[conint(strict=True, le=max(QUESTION.get("question_style").keys()), ge=min(QUESTION.get("question_style").keys()))]]
    course_ids: Optional[List[conint(strict=True)]]
    question_type: Optional[List[conint(strict=True, le=max(QUESTION.get("question_type").keys()), ge=min(QUESTION.get("question_type").keys()))]]
    answer_type: Optional[List[conint(strict=True, le=max(QUESTION.get("answer_type").keys()), ge=min(QUESTION.get("answer_type").keys()))]]


class GetAllQuestionInbound(BaseModel):
    """serializer for get all"""
    page: Optional[conint(strict=True, ge=1)] = 1
    size: Optional[conint(strict=True, ge=1)] = 50
    filter: Optional[QuestionAllFilterInbound] = {}


class QuestionFinalOutBound(SuccessResponsePartial):
    """question list outbound"""
    data: Optional[List[QuestionOutBound]]
