from coloredlogs import install
from logging import info, warning, error, INFO, ERROR, WARNING
    
class Logger:
    @staticmethod
    def log(message, level=INFO):
        install()
        if level == INFO: info(message)
        elif level == WARNING: warning(message)
        elif level == ERROR: error(message)