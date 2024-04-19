import os
from llama_parse import LlamaParse
from llama_index.readers.file import UnstructuredReader
from pydantic import BaseModel, Field, field_validator
from llama_index.core.readers import SimpleDirectoryReader
from pathlib import Path
from llama_index.core.schema import Document

# ** PARSERS **


def llama_parse_parser():
    if os.getenv("LLAMA_CLOUD_API_KEY") is None:
        raise ValueError(
            "LLAMA_CLOUD_API_KEY environment variable is not set. "
            "Please set it in .env file or in your shell environment then run again!"
        )
    parser = LlamaParse(result_type="markdown", verbose=True, language="en")
    return parser


def unstructured_loader():
    if os.getenv("UNSTRUCTURED_API_KEY") is None:
        raise ValueError(
            "UNSTRUCTURED_API_KEY environment variable is not set. "
            "Please set it in .env file or in your shell environment then run again!"
        )
    # import nltk
    # nltk.download("averaged_perceptron_tagger", download_dir="C:\\Users\\rodri\\InXploit\\BlazzmoTech\\web\\assudit\\backend\\.venv\\Lib\\site-packages\\llama_index\\core\\_static/nltk_cache")

    loader = UnstructuredReader(
        url='https://blazzbyte-1m9qxd4x.api.unstructuredapp.io', api_key=os.getenv("UNSTRUCTURED_API_KEY"))
    return loader

# ** TYPE VALIDATOR **


class FileLoaderConfig(BaseModel):
    data_dir: str = Field(
        "data", description="Directory where files are stored")
    user_id: str = Field(
        default='default', description="here goes the user id for session to be able of charge their own laws")
    use_llama_parse: bool = Field(
        False, description="Whether to use Llama parse")
    use_unstructured: bool = Field(
        False, description="Whether to use unstructured")

    @field_validator("data_dir")
    def data_dir_must_exist(cls, value):
        if not os.path.isdir(value):
            raise ValueError(f"Directory '{value}' does not exist")
        return value


# ** GET FILE DOCUMENTS **
def get_file_documents(config: FileLoaderConfig):
    """get_file_documents: Used to get a Docs objects from PDFs from a directory"""

    if config.use_llama_parse:

        import nest_asyncio

        nest_asyncio.apply()

        reader = SimpleDirectoryReader(
            input_dir=config.data_dir,
            recursive=True,
        )
        parser = llama_parse_parser()
        reader.file_extractor = {".pdf": parser}
        docs = reader.load_data()
        documents = []
        for doc in docs:
            doc.metadata['user_id'] = config.user_id
            documents.append(doc)
        return docs

    elif config.use_unstructured:
        all_docs = []

        pdf_files = list(Path(config.data_dir).glob("*.pdf"))

        loader = unstructured_loader()

        for pdf_file in pdf_files:
            docs = loader.load_data(file=pdf_file, extra_info={'user_id': config.user_id}, split_documents=False)

            for doc in docs:
                all_docs.append(doc)

        return all_docs

    else:
        raise ValueError("Select a valid loader")
