import os
import shutil
from fastapi import APIRouter, File, UploadFile, Form, Depends, Request
from typing import List, Annotated
from pydantic import BaseModel, Field

# Import the required functions for processing the uploaded documents
from app.engine.loaders.file import get_file_documents, FileLoaderConfig
from app.engine.index import get_index

from app.utils.as_form import as_form

upload_router = r = APIRouter()


class DocumentUpload(BaseModel):
    files: List[UploadFile]
    user_id: str
    use_llama_parse: bool
    use_unstructured: bool

    @classmethod
    async def get_fields(cls, request: Request):
        form = await request.form()
        files: List[UploadFile] = []
        for field_name, field_value in form.items():
            if field_name.startswith("file-"):
                files.append(field_value)

        user_id = form.get("user_id", "default").lower()
        # Other fields
        use_llama_parse = form.get("use_llama_parse", "").lower() == "true"
        use_unstructured = form.get("use_unstructured", "").lower() == "true"

        return cls(files=files, user_id=user_id, use_llama_parse=use_llama_parse, use_unstructured=use_unstructured)


@r.post("")
async def upload(data: DocumentUpload = Depends(DocumentUpload.get_fields)):

    data_dir: str = "tmp"
    os.makedirs(data_dir, exist_ok=True)

    for file in data.files:
        if file is not None:
            file_path = os.path.join(data_dir, file.filename)
            with open(file_path, "wb") as buffer:
                contents = await file.read()
                buffer.write(contents)
        else:
            print("File is None. Skipping...")
    # Prepare the configuration for the file loader
    config = FileLoaderConfig(
        data_dir=data_dir,
        user_id=data.user_id,
        use_llama_parse=data.use_llama_parse,
        use_unstructured=data.use_unstructured,
    )

    try:
        # Load the documents
        documents = get_file_documents(config)

        for document in documents:
            new_metadata = {key if key != 'filename' else 'title': document.metadata[key] for key in [
                'user_id', 'filename'] if key in document.metadata}
            document.metadata = new_metadata

        # Create index from documents
        get_index().from_documents(documents)

        # Clean up the temporary directory
        shutil.rmtree(data_dir)

        return {"message": "Documents processed successfully"}
    except Exception as e:
        # Clean up the temporary directory in case of an error
        shutil.rmtree(data_dir)
        raise e


@r.post("/document")
async def upload(file: Annotated[UploadFile, File()], user_id: Annotated[str, Form()]):

    data_dir: str = user_id
    os.makedirs(data_dir, exist_ok=True)

    if file is not None:
        file_path = os.path.join(data_dir, file.filename)
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
    else:
        print("File is None. Skipping...")

    return {"message": "Documents processed successfully"}
