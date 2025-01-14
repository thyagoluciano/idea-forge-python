# main.py
import time
import threading

from src.adapters.extraction_scheduler import ExtractionScheduler
from src.adapters.database_adapter import DatabaseAdapter
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    extraction_scheduler = ExtractionScheduler()
    extraction_thread = threading.Thread(target=extraction_scheduler.start)
    extraction_thread.start()

    database_adapter = DatabaseAdapter()

    configs = database_adapter.get_all_extraction_configs()
    for config in configs:
        if config.subreddit_name == "entrepreneur":
            extraction_scheduler.run_extraction_now(config)

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        extraction_scheduler.shutdown()
        extraction_thread.join()


if __name__ == "__main__":
    main()
