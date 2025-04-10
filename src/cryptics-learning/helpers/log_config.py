import logging

"""
Logging configurations
"""


def setup_logger(name: str = None) -> logging.Logger:
    """Set up a simple logger that prints to the terminal.

    Args:
    ----
        name (str, optional): The logger name. Use None for root logger.

    Returns:
    -------
        logging.Logger: Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # Set the handler's log level to DEBUG

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(ch)

    return logger


if __name__ == "__main__":
    # Set up the logger
    logger = setup_logger()

    # Example of logging something
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
