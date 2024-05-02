from ResearchBot.constants import *
from ResearchBot.entity.config_entity import *
from ResearchBot.utils.common import *


class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH
        # papers_filepath = PAPERS_FILE_PATH,
        # schema_filepath = SCHEMA_FILE_PATH)
    ):
        print(config_filepath)
        self.config = read_yaml(config_filepath)
        # self.papers = read_txt(papers_filepath)
        # self.schema = read_yaml(schema_filepath)

        # create_directories([self.config.artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])
        papers = read_txt(config.papers_path)
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            papers_path = config.papers_path,
            papers = papers

        )

        return data_ingestion_config
    
    def get_vector_index_config(self) -> VectorIndexConfig:
        config = self.config.vector_db

        # create_directories([config.root_dir])
        vector_index_config = VectorIndexConfig(
            root_dir=config.root_dir,
            embedding_model = config.embedding_model,
            cache_dir = config.cache_dir,
            db_name = config.db_name,
            batch_size = config.batch_size

        )
        return vector_index_config
    
    
