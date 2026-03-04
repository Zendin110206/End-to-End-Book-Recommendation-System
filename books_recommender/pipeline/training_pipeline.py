import sys
from books_recommender.components.stage_00_data_ingestion import DataIngestion
from books_recommender.exception.exception_handler import AppException


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        
    def start_training_pipeline(self):
        try:
            self.data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise AppException(e, sys) from e

    
   