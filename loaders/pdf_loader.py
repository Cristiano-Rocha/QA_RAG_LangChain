from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser

import config

loader = GenericLoader(
    blob_loader=FileSystemBlobLoader(
        path=config.DOCUMENTS_PATH,
        glob=config.DOCUMENTS_GLOB,
    ),
    blob_parser=PyPDFParser(),
)
