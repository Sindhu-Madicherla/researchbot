from ResearchBot import logger
from ResearchBot.pipeline.stage01_load_articles import DataIngestionPipeline
from ResearchBot.pipeline.stage02_vector_index import VectorIndexPipeline

STAGE_NAME = "Data Ingestion"
try:
   logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionPipeline()
   documents = data_ingestion.main()
   logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e
     
STAGE_NAME = "Vector Index Creation"
try:
   logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<") 
   vector_index = VectorIndexPipeline()
   vector_index.main(documents=documents)
   logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e