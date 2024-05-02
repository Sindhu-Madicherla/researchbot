from ResearchBot.components.vector_index import *
from ResearchBot.entity.config_entity import *
from ResearchBot.config.configuration import ConfigurationManager

class VectorIndexPipeline :

    def __init__(self):
        pass
    
    def main(self,documents):
        # Initiate the Class or config manager - configs - paper IDs, location where they have to stored
        # Call the method to download papers to the folder mentioned in theb config
        
        config = ConfigurationManager()
        vector_index_config = config.get_vector_index_config()
        vector_index = VectorIndex(config=vector_index_config)
        vector_index.create_vector_db()
        index = vector_index.get_vector_index(documents=documents)


