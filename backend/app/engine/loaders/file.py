import os
from llama_parse import LlamaParse
from llama_index.readers.file import UnstructuredReader
from pydantic import BaseModel, Field, field_validator

# ** PARSERS **


def llama_parse_parser():
    if os.getenv("LLAMA_CLOUD_API_KEY") is None:
        raise ValueError(
            "LLAMA_CLOUD_API_KEY environment variable is not set. "
            "Please set it in .env file or in your shell environment then run again!"
        )
    parser = LlamaParse(result_type="markdown", verbose=True, language="en")
    return parser


def Unstructured_parser():
    if os.getenv("UNSTRUCTURED_API_KEY") in None:
        raise ValueError(
            "UNSTRUCTURED_API_KEY environment variable is not set. "
            "Please set it in .env file or in your shell environment then run again!"
        )
    parser = UnstructuredReader(
        api=True, url='https://api.unstructured.io', api_key=os.getenv("UNSTRUCTURED_API_KEY"))
    return parser

# ** MODEL **


class FileLoaderConfig(BaseModel):
    data_dir: str = Field(
        "data", description="Directory where files are stored")
    use_llama_parse: bool = Field(
        False, description="Whether to use Llama parse")
    use_unstructured: bool = Field(
        False, description="Whether to use unstructured")

    @field_validator("data_dir")
    def data_dir_must_exist(cls, value):
        if not os.path.isdir(value):
            raise ValueError(f"Directory '{value}' does not exist")


# ** GET FILE DOCUMENTS **
def get_file_documents(config: FileLoaderConfig):
    """
    get_content_from_documents: Used to obtain the content of PDF files from a directory
    """
    from llama_index.core.readers import SimpleDirectoryReader

    print(config.data_dir)

    reader = SimpleDirectoryReader(
        input_dir=config.data_dir,
        recursive=True,
    )
    if config.use_llama_parse:
        parser = llama_parse_parser()
        reader.file_extractor = {".pdf": parser}
    elif config.use_unstructured:
        parser = Unstructured_parser()
        parser.file_extractor = {".pdf": parser}

    return reader.load_data()
