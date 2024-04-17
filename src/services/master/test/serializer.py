"""serialzier file for master test"""
from typing import Optional, List
from pydantic import BaseModel
from pydantic.types import conint

from src.utils.common_serializer import SuccessResponsePartial


class SectionInbound(BaseModel):
    """Section inbound serializer"""
    id: Optional[conint(gt=0)]
    name: str


class SectionSingleOutbound(BaseModel):
    """Section single outbound"""
    id: Optional[int]
    name: Optional[str]
    name_key: Optional[str]


class SectionListOutbound(SuccessResponsePartial):
    """Section single outbound"""
    data: Optional[List[SectionSingleOutbound]]


class SectionFinalOutbound(SuccessResponsePartial):
    """Section single outbound"""
    data: Optional[SectionSingleOutbound]


class TestDirectionInbound(BaseModel):
    """test direction model"""
    id: Optional[int]
    domain_id: Optional[int]  # nedd to apply validtaion
    test_type: Optional[int]  # need to apply validation
    direction: Optional[str]


class TestDirectionSingleOutbound(BaseModel):
    """test Direction single outbound"""
    id: Optional[int]
    domain_id: Optional[int]
    test_type: Optional[int]
    direction: Optional[str]


class TestDirectionListOutbound(SuccessResponsePartial):
    """test Direction single outbound"""
    data: Optional[List[TestDirectionSingleOutbound]]


class TestDirectionFinalOutbound(SuccessResponsePartial):
    """test Direction single outbound"""
    data: Optional[TestDirectionSingleOutbound]


class TestExplanationInbound(BaseModel):
    id: Optional[conint(gt=0)]
    test_type: Optional[int]
    explanation: Optional[str]


class TestExplanationSingleOutbound(BaseModel):
    """test explanation single outbound"""
    id: Optional[int]
    explanation: Optional[str]
    test_type: Optional[int]


class TestExplanationListOutbound(SuccessResponsePartial):
    """test explanation list outbound"""
    data: Optional[List[TestExplanationSingleOutbound]]


class TestExplanationFinalOutbound(SuccessResponsePartial):
    """test explanation final outbound"""
    data: Optional[TestExplanationSingleOutbound]
