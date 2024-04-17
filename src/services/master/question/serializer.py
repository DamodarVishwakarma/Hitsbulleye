"""serializer file for question master"""
from typing import Optional, List
from pydantic import BaseModel
from pydantic.types import conint
from src.utils.common_serializer import SuccessResponsePartial


class CourseInbound(BaseModel):
    """area inbound serializer"""
    id: Optional[conint(gt=0)]
    name: str


class CourseSingleOutbound(BaseModel):
    """area single outbound"""
    id: Optional[int]
    name: Optional[str]


class CourseListOutbound(SuccessResponsePartial):
    """area single outbound"""
    data: Optional[List[CourseSingleOutbound]]


class CourseFinalOutbound(SuccessResponsePartial):
    """area single outbound"""
    data: Optional[CourseSingleOutbound]


class AreaInbound(BaseModel):
    """area inbound serializer"""
    id: Optional[conint(gt=0)]
    area_code: Optional[str]
    area_type: Optional[int]
    name: str


class AreaSingleOutbound(BaseModel):
    """area single outbound"""
    id: Optional[int]
    name: Optional[str]
    area_code: Optional[str]
    area_type: Optional[int]


class AreaListOutbound(SuccessResponsePartial):
    """area single outbound"""
    data: Optional[List[AreaSingleOutbound]]


class AreaFinalOutbound(SuccessResponsePartial):
    """area single outbound"""
    data: Optional[AreaSingleOutbound]


class AreaDirectionInbound(BaseModel):
    """area inbound serializer"""
    id: Optional[conint(gt=0)]
    area_id: conint(gt=0)
    text: str


class AreaDirectionSingleOutbound(BaseModel):
    """area single outbound"""
    id: Optional[int]
    text: Optional[str]
    area_id: Optional[int]


class AreaDirectionListOutbound(SuccessResponsePartial):
    """area single outbound"""
    data: Optional[List[AreaDirectionSingleOutbound]]


class AreaDirectionFinalOutbound(SuccessResponsePartial):
    """area single outbound"""
    data: Optional[AreaDirectionSingleOutbound]
