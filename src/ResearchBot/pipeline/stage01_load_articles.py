from ResearchBot.components.load_data import *

from ResearchBot.entity.config_entity import *
from ResearchBot.config.configuration import ConfigurationManager

# Load, Transform, Embed > Vector Store > Ingestion Pipeline > Retrievers > Chat Session

class LoadDataPipeline :
    
    def __init__(self):
        pass
    
    def main(self):
        # Initiate the Class or config manager - configs - paper IDs, loaction where they have to stored
        # Call the method to download papers to the folder mentioned in theb config
        
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestionConfig(config:data_ingestion_config)
        data_ingestion.download_pdf()
        data_ingestion.load_arxiv_document()



#### Write different types of ingestion.
### Ingesting from archives, ingesting from wikipedia, ingesting from local folder, ingesting by 
### wrapping up a folder, from a continuous sources of API (like Twitter, reddit, essays from papers etc.)
         

        
        
    

