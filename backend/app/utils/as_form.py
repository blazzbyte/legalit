from typing import Type
from fastapi import Form, HTTPException
from pydantic import BaseModel, ValidationError
from starlette.status import HTTP_400_BAD_REQUEST
import inspect
from typing import Any, Annotated, List
from fastapi import UploadFile

def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, field in cls.__fields__.items():
        field_default = Form(default=field.default) if not field.is_required() else Form(...)
        new_parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=field_default,
                annotation=inspect.Parameter.empty,
            )
        )

    async def as_form_func(**data):
        try:
            # Convertir los campos a los tipos de datos correctos
            for field_name, field in cls.__fields__.items():
                if field_name in data:
                    if field_name == "files" and isinstance(data[field_name], str):
                        # Convertir el string a una lista de UploadFile
                        file_strings = data[field_name].split(",")
                        data[field_name] = [UploadFile(file=filename) for filename in file_strings]
                    elif field_name == "use_llama_parse":
                        data[field_name] = data[field_name].lower() == "true"
                    elif field_name == "use_unstructured":
                        data[field_name] = data[field_name].lower() == "true"
                    # Puedes agregar más conversiones de tipos según sea necesario

            return cls(**data)
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
