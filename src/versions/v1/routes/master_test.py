"""routes for area"""
from fastapi import APIRouter, Request, Response, status
from src.services.master.test.controller import TestMasterController
from src.services.master.test.serializer import SectionInbound, TestDirectionInbound, TestExplanationInbound
from src.utils.auth import Auth

router = APIRouter()


@router.post("/section/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save_section(request: Request, payload: SectionInbound):
    """route to save section"""
    return await TestMasterController.save_section(payload=payload)


@router.get("/section")
@Auth.authenticate_user
@Auth.authorize_user
async def get_section(request: Request, id: int = None, name: str = None):
    """route to get area by id"""
    if id:
        return await TestMasterController.get_section_by_id(_id=id)
    else:
        return await TestMasterController.get_section_list(search_term=name)


@router.delete("/section/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def delete_section(request: Request, id: int):
    """route to delete area"""
    await TestMasterController.delete_section(_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/test-direction/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save_test_direction(request: Request, payload: TestDirectionInbound):
    """route to save course"""
    return await TestMasterController.save_test_direction(payload=payload)


@router.get("/test-direction")
@Auth.authenticate_user
@Auth.authorize_user
async def get_test_direction(request: Request, _id: int = None, domain_id: int = None, test_type: int = None):
    """route to get test directions"""
    return await TestMasterController.get_test_direction(_id=_id, domain_id=domain_id, test_type=test_type)


@router.delete("/test-direction/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def delete_test_direction(request: Request, id: int):
    """route to delete course by id"""
    await TestMasterController.delete_test_direction(_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.post("/test_explanation/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save_test_explanation(request: Request, payload: TestExplanationInbound):
    """route to save course"""
    return await TestMasterController.save_test_explanation(payload=payload)


@router.get("/test_explanation/")
@Auth.authenticate_user
@Auth.authorize_user
async def get_test_explanation_list(request: Request, search_term: str = None):
    """route to get test explanation list"""
    return await TestMasterController.get_test_explanation_list(search_term=search_term)


@router.get("/test_explanation/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def get_course_list(request: Request, id: int):
    """route to get test explanation by id"""
    return await TestMasterController.get_test_explanation_by_id(_id=id)


@router.delete("/test_explanation/{id}")
@Auth.authenticate_user
@Auth.authorize_user
async def delete_test_explanation(request: Request, id: int):
    """route to delete test explanation by id"""
    await TestMasterController.delete_test_explanation(_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

