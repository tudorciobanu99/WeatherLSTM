import logging
import os
from datetime import datetime

class Logger():
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(self.name)
        self._set_file_handler()

    def _set_file_handler(self):
        os.makedirs('logs', exist_ok=True)
        filename = f'logs/{datetime.now().strftime('%Y-%m-%d')}_{self.name}.log'
        fileHandler = logging.FileHandler(filename)
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(self._get_formatter())
        self.logger.addHandler(fileHandler)

    def _get_formatter(self):
        return logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        )
    
    def get_logger(self) -> logging.Logger:
        return self.logger