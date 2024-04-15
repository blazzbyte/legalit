import os
import shutil
from fastapi import APIRouter, File, UploadFile, Form, Depends
from typing import List, Annotated
from pydantic import BaseModel, Field

# Import the required functions for processing the uploaded documents
from app.engine.loaders.file import get_file_documents, FileLoaderConfig
from app.engine.index import get_index

from app.utils.as_form import as_form

upload_router = r = APIRouter()

@as_form
class DocumentUpload(BaseModel):
    files: List[UploadFile] = Field(..., description="List of files to upload")
    use_llama_parse: bool = Field(..., description="Whether to use Llama parse")
    use_unstructured: bool = Field(..., description="Whether to use unstructured")

@r.post("")
async def upload(docs: DocumentUpload = Depends(DocumentUpload.as_form)):
    print(type(docs.use_llama_parse))
    data_dir = "tmp"
    os.makedirs(data_dir, exist_ok=True)

    for file in docs.files:
        file_path = os.path.join(data_dir, file.filename)
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)

    # Prepare the configuration for the file loader
    config = FileLoaderConfig(
        data_dir=data_dir,
        use_llama_parse=docs.use_llama_parse,
        use_unstructured=docs.use_unstructured,
    )

    try:
        # Load the documents
        documents = get_file_documents(config)

        # Create index from documents
        index = get_index()
        index.from_documents(documents)

        # Clean up the temporary directory
        shutil.rmtree(data_dir)

        return {"message": "Documents processed successfully"}
    except Exception as e:
        # Clean up the temporary directory in case of an error
        shutil.rmtree(data_dir)
        raise e
