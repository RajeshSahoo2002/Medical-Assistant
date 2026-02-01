import logging

def setup_logger(name="AI_Medical_Assistant"):
    logger=logging.getLogger(name)
    # logger.debug is used to get catch of all the logs at the debug level which is used to track any error/messages.
    logger.setLevel(logging.DEBUG)
    
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter=logging.Formatter("[%(asctime)s][%(levelname)s] --- [%(message)s]")
    ch.setFormatter(formatter)
    
    # Below if logic is to give different messages while everytime logger file sends the logs. Basically to give a unique message every time.
    if not logger.hasHandlers():
        logger.addHandler(ch)
    return logger

logger=setup_logger()
logger.debug("Logs are being debugged")
logger.error("Failed to load the logs")
logger.critical("Critical issue found in the logs")
logger.info("RAG process started")