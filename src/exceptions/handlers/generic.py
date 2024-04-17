"""Centralized exception handeling"""
from fastapi import Request, status
from starlette.responses import JSONResponse
from src.main import app
from src.exceptions.errors.generic import (
    EntityException,
    Unauthenticated,
    UnauthenticatedForbidden,
    Unauthorized,
    FormParseException
)

@app.exception_handler(FormParseException)
async def form_parse_exception_handler(request: Request, exe: FormParseException):
    """form parse exception handler"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "failure",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": exe.message,
        },
    )


@app.exception_handler(EntityException)
async def entity_not_found_exception_handler(request: Request, exc: EntityException):
    """Entity not found exception handler"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": exc.message,
        },
    )

@app.exception_handler(Unauthenticated)
async def unauthenticated_exception_handler(request: Request, exc: Unauthenticated):
    """unauthenticated exception handler"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "status": "failure",
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": exc.message,
        },
    )


@app.exception_handler(UnauthenticatedForbidden)
async def unauthenticated_exception_handler_forbidden(request: Request, exc: UnauthenticatedForbidden):
    """unauthenticated exception handler forbidden"""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "status": "failure",
            "code": status.HTTP_403_FORBIDDEN,
            "message": exc.message,
        },
    )


@app.exception_handler(Unauthorized)
async def unauthorized_exception_handler(request: Request, exc: Unauthorized):
    """unauthorized exception handler"""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "status": "failure",
            "code": status.HTTP_403_FORBIDDEN,
            "message": "Unauthorized Request!",
        },
    )
