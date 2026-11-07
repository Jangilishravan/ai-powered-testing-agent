import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/test_execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logger = logging.getLogger(__name__)