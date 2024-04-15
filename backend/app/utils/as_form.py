from typing import Type
from fastapi import Form, HTTPException
from pydantic import BaseModel
from pydantic import ValidationError
from starlette.status import HTTP_400_BAD_REQUEST
import inspect

def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, field in cls.model_fields.items():
        field_default = Form(...)
        new_parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(field.default) if not field.is_required() else field_default,
                annotation=inspect.Parameter.empty,
            )
        )

    async def as_form_func(**data):
        try:
            return cls.model_construct(**data)
        except ValidationError as e:
            first_error = e.errors()[0]
            error_message = first_error['msg']
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, 
                detail=error_message
            )

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig
    setattr(cls, 'as_form', as_form_func)
    return cls