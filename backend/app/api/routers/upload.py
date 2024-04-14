import os
import shutil
from fastapi import APIRouter, File, UploadFile, Form
from typing import List
from pydantic import BaseModel, Field

# Import the required functions for processing the uploaded documents
from backend.app.engine.loaders.file import get_file_documents, FileLoaderConfig
from app.engine.index import get_index

router = APIRouter()

class DocumentUpload(BaseModel):
    files: List[UploadFile] = Field(..., description="List of files to upload")
    use_llama_parse: bool = Field(..., description="Whether to use Llama parse")
    use_unstructured: bool = Field(..., description="Whether to use unstructured")

@router.post("")
async def upload_documents(docs: DocumentUpload):
    # Create a temporary directory to store the uploaded files
    data_dir = "tmp"
    os.makedirs(data_dir, exist_ok=True)

    # Save the uploaded files to the temporary directory
    file_paths = []
    for file in docs.files:
        file_path = os.path.join(data_dir, file.filename)
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
        file_paths.append(file_path)

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