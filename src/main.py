# src/main.py
import time
import threading
import uvicorn

from src.adapters.extraction_scheduler import ExtractionScheduler
from src.adapters.analysis_scheduler import AnalysisScheduler
from src.adapters.database_adapter import DatabaseAdapter
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    extraction_scheduler = ExtractionScheduler()
    extraction_thread = threading.Thread(target=extraction_scheduler.start)
    extraction_thread.start()

    # Inicia o scheduler de analise
    analysis_scheduler = AnalysisScheduler()
    analysis_thread = threading.Thread(target=analysis_scheduler.start)
    analysis_thread.start()

    # Força a execução imediata de uma extração

    database_adapter = DatabaseAdapter()
    configs = database_adapter.get_all_extraction_configs()
    for config in configs:
        if config.subreddit_name == "askcarsales":
            extraction_scheduler.run_extraction_now(config)

    analysis_scheduler.run_analysis_now()

    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        extraction_scheduler.shutdown()
        analysis_scheduler.shutdown()
        extraction_thread.join()
        analysis_thread.join()


def run_api():
    """Runs the FastAPI application."""
    import src.adapters.api.main as api
    uvicorn.run(api.app, host="0.0.0.0", port=8081)


if __name__ == "__main__":
    main()
