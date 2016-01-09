import sys
import logging

logger = logging.getLogger("data")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)
