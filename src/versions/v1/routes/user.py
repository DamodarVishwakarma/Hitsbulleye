"""routes for user"""
from fastapi import APIRouter, Request
from typing import Optional
from src.services.user.controller import UserController
from src.services.user.serializer import UserCommonInBound
from src.utils.auth import Auth

router = APIRouter()


@router.post("/save")
@Auth.authenticate_user
@Auth.authorize_user
async def save(request: Request, payload: UserCommonInBound):
    """route to save user"""
    return await UserController.save(payload=payload)


@router.get('/{email}')
@Auth.authenticate_user
@Auth.authorize_admin
async def get_user(request: Request, email: Optional[str]):
    """
    API to Get users by email
    """
    return await UserController.get_by_email_and_id(emails=[email])
