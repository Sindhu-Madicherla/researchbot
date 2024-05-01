import os
import json
import arxiv
import requests
import fitz
from pymupdf_rag import to_markdown
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


<<<<<<< HEAD
from chatxiv-project.entity.config_entity import LoadDataConfig
=======
from ResearchBot.entity.config_entity import DataIngestionConfig
>>>>>>> 8173d6e (Changes)


os.environ['OPENAI_API_KEY'] = '***'

class DataIngestion:
    
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.arxiv_client = arxiv.Client()

    def download_pdf(self):
        '''Downloads a paper from arXiv given its ID'''
        paper = next(arxiv.Client().results(arxiv.Search(id_list=[paper_id])))
        return paper.download_pdf(dirpath=dirpath), paper
    
    def load_arxiv_document(self, paper_id):
        '''Loads an arxiv paper as a Document object'''
        pdf_path, paper = self.download_pdf(paper_id, dirpath='./papers')
        paper_pdf = fitz.open(pdf_path)
        md_text = to_markdown(paper_pdf)
        
        return Document(
            doc_id=paper_id,
            text=md_text,
            metadata={
                'title': paper.title,
                'authors': ", ".join([auth.name for auth in paper.authors[:10]]),
                'published': paper.published.strftime('%Y-%m-%d'),
                'filepath': pdf_path,
            }
        )
        
    

    