import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Create logger
    logger = logging.getLogger("fastapi_chatbot_logger")
    logger.setLevel(log_level)

    # Ensure logs directory exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, "app.log")

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # Create file handler which logs even debug messages
    fh = RotatingFileHandler(log_file_path, maxBytes=10485760, backupCount=5) # 10MB per file, 5 backups
    fh.setLevel(log_level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.handlers: # Prevent adding duplicate handlers if setup_logging is called multiple times
        logger.addHandler(ch)
        logger.addHandler(fh)
    
    return logger

# Initialize logger
logger = setup_logging()

# Example usage (for testing purposes)
if __name__ == "__main__":
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
