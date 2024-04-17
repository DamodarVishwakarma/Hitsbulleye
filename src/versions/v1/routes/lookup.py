"""routes for lookup"""
from enum import Enum
from fastapi import APIRouter, Request, Depends
from typing import Set
from src.services.lookup.controller import LookupController
from src.services.lookup.serializer import Model
from src.utils.auth import Auth

router = APIRouter()


def parse_list(param_name: str):
    """Parse list"""
    def parse(request: Request):
        try:
            return request.query_params[param_name].split(",")
        except KeyError:
            return []
    return parse


@router.get("/")
@Auth.authenticate_user
@Auth.authorize_user
async def get_lookup_data(request: Request, models: Set[Model] = Depends(parse_list("models"))):
    """route to save user"""
    return await LookupController.get_lookup_data(models=models)
