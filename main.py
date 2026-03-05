from books_recommender.pipeline.training_pipeline import TrainingPipeline
import sys
from books_recommender.exception.exception_handler import AppException
import books_recommender.logger.log as log_config
import logging

try:
    logging.info("Memulai proses pelatihan model rekomendasi buku...")
    pipeline = TrainingPipeline()
    pipeline.start_training_pipeline()
    logging.info("Proses pelatihan model selesai.")
except Exception as e:
    logging.info(error_message := f"Kesalahan terjadi selama pelatihan model: {e}")
    raise AppException(e, sys) from e