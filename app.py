import sys
from books_recommender.exception.exception_handler import AppException
import books_recommender.logger.log as log_config
import logging

def jalankan_pabrik():
    try:

        logging.info("Pabrik mulai beroperasi. CCTV diaktifkan.")
        logging.info("Pekerja sedang mencoba membagi angka 1 dengan 0...")
        
        a = 1 / 0
        
    except Exception as e:
        
        logging.info(error_message := f"Kesalahan terjadi: {e}. CCTV merekam kejadian ini.")
        
        
        raise AppException(e, sys)

if __name__ == "__main__":
    jalankan_pabrik()