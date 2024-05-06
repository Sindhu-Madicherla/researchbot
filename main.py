from ResearchBot import logger
from ResearchBot.pipeline.embed_articles import DataIngestionPipeline
from ResearchBot.pipeline.stage02_vector_index import VectorIndexPipeline
from ResearchBot.pipeline.retrieval import ResponsePipeline

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
   index = vector_index.main(documents=documents)
   logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

# STAGE_NAME = "ResponseSynthesis"
# try:
#    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<") 
#    response_synthesis = ResponsePipeline()
#    response_synthesis.main(index=index)
#    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#         logger.exception(e)
#         raise e