import arxiv
import fitz
from ResearchBot.utils.to_markdown import to_markdown
import chromadb
from llama_index.core import Document
from dotenv import load_dotenv
import chromadb
import tiktoken
import openai
import numpy as np
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import MarkdownNodeParser
import chromadb.utils.embedding_functions as embedding_functions
from ResearchBot.variables.configs import Configs
from ResearchBot.utils.common import *


os.environ['OPENAI_API_KEY'] = Configs.open_API_Key


class DataIngestion:
    
    def __init__(self,papers):
        self.arxiv_client = arxiv.Client()
        self.papers = papers
        
    def num_tokens_from_text(text: str, encoding_name="cl100k_base"):
            """
            Returns the number of tokens in a text string.
            """
            encoding = tiktoken.get_encoding(encoding_name)
            num_tokens = len(encoding.encode(text))
            if num_tokens > 8000 :
                print(str)
                print(num_tokens)

    def get_papers_from_arxiv(self,topic):
        print(topic)
        search = arxiv.Search(
                    query = topic,
                    max_results = Configs.arxiv_max_results,
                    sort_by = arxiv.SortCriterion.SubmittedDate
                    )
        results = self.arxiv_client.results(search)
        papers=list(results)
        papers_list = [r.entry_id.replace('http://arxiv.org/abs/','').replace('v1','') for r in papers]    
        return papers_list, papers
    
    def download_pdf(self):
        '''Downloads a paper from arXiv given its ID'''
        papers=self.papers
        create_directories([Configs.articles_dir])
        papers_list = papers.split(',') if ',' in papers else papers.split('-')
        print(papers_list)
        if "topic" in papers_list[0]:
            papers_list, papers = self.get_papers_from_arxiv(papers_list[1])
        else : 
            papers = list(self.arxiv_client.results(arxiv.Search(id_list=papers_list)))
        return [(paper_id, paper.download_pdf(dirpath=Configs.articles_dir), paper) for (paper_id,paper) in zip(papers_list,papers)]
    
    def load_arxiv_documents(self):
        '''Loads an arxiv paper as a Document object'''
        papers = self.download_pdf()
        documents=[]
        
        for (paper_id,pdf_path,paper) in papers:
            paper_pdf = fitz.open(pdf_path)
            md_text = to_markdown(paper_pdf)
            if len(md_text.split(' ')) > 5000 :
                splits = md_text.split(' ')
                md_texts = [splits[i:i + 5000] for i in range(0, len(splits), 5000)]
                for text in md_texts:
                    print(len(text))
                    md_text = " ".join(text)
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
    
    def create_or_get_vector_db(self):
        '''Creates or gets the Chroma DB and instantiates Vector Store, Docstore, and Open AI embeding model'''
        
        # Creating a Chroma VectorDB instance
        db = chromadb.PersistentClient(path=Configs.db_dir)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                        api_key=Configs.open_API_Key,
                        model_name=Configs.embedding_model
                    )
        chroma_collection = db.get_or_create_collection(Configs.db_name, embedding_function=openai_ef)
        self.vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        self.docstore = SimpleDocumentStore()
        self.embed_model = OpenAIEmbedding(model=Configs.embedding_model, embed_batch_size=Configs.batch_size)
        
        
    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3), retry=retry_if_not_exception_type(openai.BadRequestError))   
    def run_pipeline(self, documents):
        '''Buolds and runs the ingesation pipeline'''
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
        pipeline.persist(Configs.cache_dir)

    def main(self):
        documents = self.load_arxiv_documents()
        self.create_or_get_vector_db()
        self.run_pipeline(documents=documents)
        
if __name__ == "__main__":
    data_ingestion = DataIngestion(papers=Configs.papers)
    data_ingestion.main()


    
    
        
    

    