import os
import json
from ResearchBot.utils.to_markdown import to_markdown
import chromadb
from llama_index.core import VectorStoreIndex, PromptTemplate
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
import chromadb.utils.embedding_functions as embedding_functions
from llama_index.core.tools import FunctionTool
from openai.types.chat.chat_completion_tool_message_param import ChatCompletionToolMessageParam
from ResearchBot.variables.configs import Configs
from ResearchBot.utils.chat import ChatLLM, ChatSession

os.environ['OPENAI_API_KEY'] = Configs.open_API_Key


class ResponseSynthesis:
    
    def __init__(self):
        self.system_prompt = {
            'role': 'system',
            'content': """You are a Q&A bot. You are here to answer questions based on the context given.
        You are prohibited from using prior knowledge and you can only use the context given. If you need 
        more information, please ask the user."""
        }
        
        self.get_index()
    
    def get_index(self):
        db = chromadb.PersistentClient(path=Configs.db_dir)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                        api_key=Configs.open_API_Key,
                        model_name=Configs.embedding_model
                    )
        chroma_collection = db.get_or_create_collection(Configs.db_name, embedding_function=openai_ef)

        # Create a Chroma VectorStore
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        embed_model = OpenAIEmbedding(model=Configs.embedding_model, embed_batch_size=Configs.batch_size)
        
        index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
        )
        self.index = index

    def retriever(self,user_query,similarity_top_k=Configs.similarity_top_k):
        retriever = self.index.as_retriever(similarity_top_k=similarity_top_k)
        retrieved_nodes = retriever.retrieve(user_query)
        return retrieved_nodes
        
    def build_context_prompt(self,retrieved_nodes):
        context_prompt = PromptTemplate(
        """Context information to answer the query is below.
        ---------------------
        {context_str}
        ---------------------""")
        context_str = "\n\n".join([r.node.get_content(metadata_mode='all') for r in retrieved_nodes])
        return context_prompt.format(
            context_str=context_str
        )   
         
    def context_retriever(self,user_query,similarity_top_k):
        '''
        This function let's you semantically retrieve relevant context chunks from a given document based on a query.

        Arguments:
            query (str): The query to search for in the document. Based on the original user query, write a good search query
                        which is more logically sound to retrieve the relevant information from the document.
            top_k (int): The number of top chunks to retrieve from the document. Default is 3. You can increase this number if
                        you feel like you need more information. But ideally you should make multiple calls to retrieve different
                        topics of information.

        Returns:
            str: The top retrieved
            List[NodeWithScore]: A list of nodes with their scores. Use this to cite the information in the response.
        '''
        retrieved_nodes = self.retriever(user_query=user_query,similarity_top_k=similarity_top_k)
        return self.build_context_prompt(retrieved_nodes), retrieved_nodes
        
    def chat(self, user_query, function_tools=False)  :
        llm = ChatLLM()
        session = ChatSession(llm, system_prompt=self.system_prompt)
        
        if function_tools==False:
            content = self.build_context_prompt(self.retriever(user_query=user_query))
            session.thread.append({
                'role': 'user',
                'content': content
            })
            
            response = session.chat(user_query)
            return response
        
        else : 
            context_retrieval_tool = FunctionTool.from_defaults(fn=self.context_retriever)
            available_functions = {
                "context_retriever": self.context_retriever,
            }
            response = session.chat(user_query, 
                                    temperature=Configs.temperature,
                                    max_tokens=Configs.max_tokens,
                                    tools=[context_retrieval_tool.metadata.to_openai_tool()], tool_choice='auto')
            
            tool_calls = response.tool_calls
            
            # Check if the model wanted to call a function
            if tool_calls:
                # Call the function
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    function_response, retrieved_nodes = function_to_call(**function_args)

                    print(f'Retrieving with {tool_call}')

                    # Add the function response to the message thread
                    session.thread.append(
                        ChatCompletionToolMessageParam(role='tool', tool_call_id=tool_call.id, name=function_name, content=function_response)
                    )
                
                # Get a new response from the model where it can see the function response
                post_function_response = session.chat()
                return post_function_response
            
            return response
  

if __name__ == "__main__":
    response_synthesis = ResponseSynthesis()
    response_synthesis.get_index()
    ques = ['Is Mamba an LLM ?','What is selective space model?', 'Is selective space mode same as vector embeddings?']
    for q in ques :   
        response = response_synthesis.chat(q,function_tools=True)
        print(response.content)


 