import logging
import os

from llama_index.indices.managed.vectara import VectaraIndex


logger = logging.getLogger("uvicorn")


def get_index():
    logger.info("Creating index from Vectara Index...")

    index = VectaraIndex(
        show_progress=True,
        use_core_api=False,
        parallelize_ingest=False,
    )
    
    logger.info("Index from Milvus created.")
    return index
