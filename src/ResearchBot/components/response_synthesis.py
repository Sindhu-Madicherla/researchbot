import os
import json
import arxiv
import requests
import fitz
from ResearchBot.utils.to_markdown import to_markdown
from typing import List, Tuple

import chromadb
from llama_index.core import Document, VectorStoreIndex, PromptTemplate
from llama_index.core.schema import NodeWithScore
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import MarkdownNodeParser
import chromadb.utils.embedding_functions as embedding_functions
# from chat_utils import ChatLLM, ChatSession
from ResearchBot.entity.config_entity import ResponseSynthesisConfig


os.environ['OPENAI_API_KEY'] = '***'

class ResponseSynthesis:
    
    def __init__(self, config: ResponseSynthesisConfig):
        self.config = config
    
    def chat():
        # Write logic
        pass


 