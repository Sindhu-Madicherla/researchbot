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
from ResearchBot.entity.config_entity import DataIngestionConfig


os.environ['OPENAI_API_KEY'] = '***'

class DataIngestion:
    
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.arxiv_client = arxiv.Client()
        # self.arxiv = arxiv

    def download_pdf(self):
        '''Downloads a paper from arXiv given its ID'''
        
        papers = list(self.arxiv_client.results(arxiv.Search(id_list=self.config.papers)))
        return [(paper_id, paper.download_pdf(dirpath=self.config.root_dir), paper) for (paper_id,paper) in zip(self.config.papers,papers)]
    
    def load_arxiv_documents(self):
        '''Loads an arxiv paper as a Document object'''
        papers = self.download_pdf()
        documents=[]
        
        for (paper_id,pdf_path,paper) in papers:
            paper_pdf = fitz.open(pdf_path)
            md_text = to_markdown(paper_pdf)
            document = Document(
                doc_id=paper_id,
                text=md_text,
                metadata={
                    'title': paper.title,
                    'authors': ", ".join([auth.name for auth in paper.authors[:10]]),
                    'published': paper.published.strftime('%Y-%m-%d'),
                    'filepath': pdf_path,
                }
            )
            
            documents.append(document)
        return documents
        
    

    