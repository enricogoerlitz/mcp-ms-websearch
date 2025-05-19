import os
import logging


filepath = None if os.environ.get("DEBUG") \
                else os.environ.get("LOGGING_FILEPATH")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(filename)s %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S,%f",
    filename=filepath
)

logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("pdfplumber").setLevel(logging.ERROR)
logging.getLogger("pdfminer").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
