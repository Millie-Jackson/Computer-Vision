# scripts/logging_config.py



import logging
import os



# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)



def setup_logger(name, log_file="logs/game.log", level=logging.INFO):
    """"""

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    handler = logging.FileHandler(log_file, mode='a')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)
    
    return logger

# End of File