import os
import json
import arxiv
import requests
import fitz
from ResearchBot.utils.to_markdown import to_markdown
from typing import List, Tuple
from dotenv import load_dotenv
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
from ResearchBot.entity.config_entity import VectorIndexConfig


os.environ['OPENAI_API_KEY'] = '***'

class VectorIndex:
    
    def __init__(self, config: VectorIndexConfig):
        self.config = config
        load_dotenv()
        
    
    def create_vector_db(self):
        
        # Creating a Chroma VectorDB instance
        db = chromadb.PersistentClient(path=self.config.root_dir)
        api_key = '***'
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                        # api_key=os.getenv("OPENAI_API_KEY"),
                        api_key=api_key,
                        model_name=self.config.embedding_model
                    )
        chroma_collection = db.get_or_create_collection(self.config.db_name, embedding_function=openai_ef)

        # Create a Chroma VectorStore
        self.vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        # Create a Simple Document Store as well
        self.docstore = SimpleDocumentStore()

        # Load the embedding model
        self.embed_model = OpenAIEmbedding(model=self.config.embedding_model, embed_batch_size=self.config.batch_size)
        
        
        
    def get_vector_index(self, documents):
        # Build the Embedding Pipeline
        parser = MarkdownNodeParser()
        pipeline = IngestionPipeline(
            transformations=[
                parser,
                self.embed_model,
            ],
            vector_store=self.vector_store,
            docstore=self.docstore,
        )
        # load local cache (if it exists)
        # pipeline.load("./pipeline_chatxiv")

        pipeline.run(documents=documents, show_progress=True)

        # save cache locally
        pipeline.persist(self.config.cache_dir)

        # An IngestionPipeline uses a concept of Transformations that are applied to input data. These Transformations are applied to your input data,
        # and the resulting nodes are either returned or inserted into a vector database (if given). Each node+transformation pair is cached, so that subsequent 
        # runs (if the cache is persisted) with the same node+transformation combination can use the cached result and save you time.

        # Create vector index for retrieval
        index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            embed_model=self.embed_model
        )

        ## This is the final index which has everything
        
        return index
        

        
    

    