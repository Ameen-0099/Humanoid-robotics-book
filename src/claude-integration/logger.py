import logging
import logging.handlers

def setup_logger():
    """
    Sets up a logger for the Claude Code integration.
    """
    logger = logging.getLogger('claude_code_integration')
    logger.setLevel(logging.INFO)

    # Create a file handler that logs even debug messages
    handler = logging.handlers.RotatingFileHandler(
        'claude_code_integration.log',
        maxBytes=1024 * 1024,
        backupCount=5
    )
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    return logger

if __name__ == '__main__':
    # Example usage:
    logger = setup_logger()
    logger.info('This is an info message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
