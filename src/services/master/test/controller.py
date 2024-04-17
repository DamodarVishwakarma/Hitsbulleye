"""controller file for Question master"""
from src.configs.error_constant import ErrorMessage
from src.exceptions.errors.generic import EntityException
from src.services.master.test.model.section import SectionModel
from src.services.master.test.model.test_direction import TestDirectionModel
from src.services.master.test.model.test_explanation import TestExplanationModel
from src.services.master.test.serializer import SectionInbound, SectionSingleOutbound, SectionFinalOutbound, \
    SectionListOutbound, TestDirectionSingleOutbound, TestDirectionListOutbound, TestDirectionInbound, \
    TestExplanationInbound, TestExplanationListOutbound, TestExplanationSingleOutbound, TestExplanationFinalOutbound, \
    TestDirectionFinalOutbound
from src.utils.common import name_key_serializer


class TestMasterController:
    """controller class for test master"""

    @classmethod
    async def save_section(cls, payload: SectionInbound):
        """method to save and update section"""
        name_key = name_key_serializer(payload.name)
        section_data = SectionModel.get_section(name_key=name_key, status=True)
        if section_data and (not payload.id or section_data.id != payload.id):
            raise EntityException(message=ErrorMessage.RECORD_ALREADY_EXISTS)
        if payload.id:
            section_data = SectionModel.get_section(_id=payload.id, status=True)
            if not section_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Section"))
        payload_dict = payload.dict(exclude_none=True, exclude_unset=True)
        payload_dict["name_key"] = name_key
        if payload.id:
            _id = payload_dict.pop("id")
            data = SectionModel.patch(_id=_id, **payload_dict)
        else:
            data = SectionModel.create(**payload_dict)
        return await cls.get_section_by_id(_id=data.id)

    @classmethod
    async def get_section_list(cls, search_term: str = None):
        """method to get area list"""
        name_key = name_key_serializer(search_term) if search_term else None
        data = SectionModel.get_section(name_key=name_key, is_all=True, limit=10)
        response = []
        for each_data in data:
            response.append(SectionSingleOutbound(
                id=each_data.id,
                name=each_data.name,
                name_key=each_data.name_key
            ))
        return SectionListOutbound(data=response)

    @classmethod
    async def get_section_by_id(cls, _id: int):
        """get section by id"""
        data = SectionModel.get_section(_id=_id, status=True)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Area"))
        response = SectionSingleOutbound(
            id=data.id,
            name=data.name,
            name_key=data.name_key
        )
        return SectionFinalOutbound(data=response)

    @classmethod
    async def delete_section(cls, _id: int):
        """get Course by id"""
        data = SectionModel.get_section(_id=_id, status=True)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Area"))
        SectionModel.patch(_id=_id, **{"status":  False})
        return True

    @classmethod
    async def save_test_direction(cls, payload: TestDirectionInbound):
        """method to save and update test direction"""
        if payload.id:
            direction_data = TestDirectionModel.get_by_id(_id=payload.id, status=True)
            if not direction_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Course"))
        payload_dict = payload.dict(exclude_none=True, exclude_unset=True)
        if payload.id:
            _id = payload_dict.pop("id")
            data = TestDirectionModel.patch(_id=_id, **payload_dict)
        else:
            data = TestDirectionModel.create(**payload_dict)
        return await cls.get_test_direction(_id=data.id)

    @classmethod
    async def get_test_direction(cls, _id: int = None, domain_id: int = None, test_type: int = None):
        """method to get Course list"""
        data = TestDirectionModel.get_by_id(_id=_id, domain_id=domain_id, test_type=test_type)
        response = []
        if _id:
            response.append(TestDirectionSingleOutbound(
                id=data.id, domain_id=data.domain_id,
                test_type=data.test_type, direction=data.direction
            ))
        else:
            for each_data in data:
                response.append(TestDirectionSingleOutbound(
                    id=each_data.id, domain_id=each_data.domain_id,
                    test_type=each_data.test_type, direction=each_data.direction
                ))
        return TestDirectionListOutbound(data=response)

    @classmethod
    async def delete_test_direction(cls, _id: int):
        """get Course by id"""
        data = TestDirectionModel.get_by_id(_id=_id, status=True)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Course"))
        TestDirectionModel.patch(_id=_id, **{"status":  False})
        return True

    @classmethod
    async def save_test_explanation(cls, payload: TestExplanationInbound):
        """method to save and update test explanation... """
        if payload.id:
            test_data = TestExplanationModel.get_by_id(_id=payload.id, status=True)
            if not test_data:
                raise EntityException(message=ErrorMessage.INVALID_ID.format("Test Explanation.."))
        payload_dict = payload.dict(exclude_none=True, exclude_unset=True)
        if payload.id:
            _id = payload_dict.pop("id")
            data = TestExplanationModel.patch(_id=_id, **payload_dict)
        else:
            data = TestExplanationModel.create(**payload_dict)
        return await cls.get_test_explanation_by_id(_id=data.id)

    @classmethod
    async def get_test_explanation_by_id(cls, _id: int = None, test_type: int = None):
        """get area by id"""
        data = TestExplanationModel.get_by_id(_id=_id, test_type=test_type, status=True)
        response = []
        if _id:
            response.append(TestExplanationSingleOutbound(
                id=data.id,
                test_type=data.test_type, explanation=data.explanation
            ))
        else:
            for each_data in data:
                response.append(TestDirectionSingleOutbound(
                    id=each_data.id,
                    test_type=each_data.test_type, explanation=each_data.explanation
                ))
        return TestExplanationListOutbound(data=response)

    @classmethod
    async def delete_test_explanation(cls, _id: int):
        """delete test explanation"""
        data = TestExplanationModel.get_by_id(_id=_id, status=True)
        if not data:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("Test Explanation"))
        TestExplanationModel.patch(_id=_id, **{"status": False})
        return True

    @classmethod
    async def get_test_explanation_list(cls, search_term: str = None):
        """method to get Course list"""
        name_key = name_key_serializer(search_term) if search_term else None
        data = TestExplanationModel.get_list(name_key=name_key)
        response = []
        for each_data in data:
            response.append(TestExplanationSingleOutbound(id=each_data.id, explanation=each_data.explanation))
        return TestExplanationListOutbound(data=response)
