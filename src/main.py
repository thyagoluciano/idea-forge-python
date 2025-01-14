# main.py
import time
import threading

from src.adapters.extraction_scheduler import ExtractionScheduler
from src.adapters.analysis_scheduler import AnalysisScheduler
from src.adapters.database_adapter import DatabaseAdapter
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    # Inicia o scheduler de extração
    extraction_scheduler = ExtractionScheduler()
    extraction_thread = threading.Thread(target=extraction_scheduler.start)
    extraction_thread.start()

    # Inicia o scheduler de analise
    analysis_scheduler = AnalysisScheduler()
    analysis_thread = threading.Thread(target=analysis_scheduler.start)
    analysis_thread.start()

    # Adiciona configurações de extração
    # database_adapter = DatabaseAdapter()

    # Força a execução imediata de uma extração
    # configs = database_adapter.get_all_extraction_configs()
    # for config in configs:
    #     if config.subreddit_name == "SaaS":
    #         extraction_scheduler.run_extraction_now(config)
    #
    analysis_scheduler.run_analysis_now()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        extraction_scheduler.shutdown()
        analysis_scheduler.shutdown()
        extraction_thread.join()
        analysis_thread.join()


if __name__ == "__main__":
    main()
