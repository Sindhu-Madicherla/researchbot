from ResearchBot.components.response_synthesis import *
from ResearchBot.entity.config_entity import *
from ResearchBot.config.configuration import ConfigurationManager

class ResponsePipeline :
    def __init__(self) -> None:
        pass
    
    def main(self,index):
        config = ConfigurationManager()
        response_synthesis_config = config.get_response_synthesis_config()
        response_synthesis = ResponseSynthesis(config=response_synthesis_config)
        response_synthesis.chat()

        # Initiate the class from Config manager - configs - vector_store location, embedding model. These can be either returned from the earlier process, or stored ? Which one is better ?
    
        # Create vector index for retrieval. ## This is the final index which has everything
        
        # Give systemprompt, build context prompt
        # Start Chat session, and ask questions
        # One method for simple chat bot
        # One method for retrieval as a tool
        # Start a streamlit application, and start asking questions there.
