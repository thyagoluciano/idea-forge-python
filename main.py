import time
import threading

from old.scheduler.extraction_scheduler import ExtractionScheduler
from old.database.database_manager import DatabaseManager
from old.scheduler.analysis_scheduler import AnalysisScheduler


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
    database_manager = DatabaseManager()
    # config_saas = {
    #     "type": "subreddit",
    #     "subreddit_name": "SaaS",
    #     "sort_criteria": "hot",
    #     "batch_size": 10,
    #     "days_ago": 1,
    #     "limit": 100,
    #     "schedule_time": "00:10",  # Horario da extração
    #     "daily": True
    # }
    # database_manager.add_extraction_config(config_saas)

    # Força a execução imediata de uma extração
    # configs = database_manager.get_all_extraction_configs()
    # for config in configs:
    #     if config.subreddit_name == "SaaS":
    #         extraction_scheduler.run_extraction_now(config)

    # Força a execução imediata da análise
    analysis_scheduler.run_analysis_now()

    # Mantém o programa rodando para o agendador funcionar
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
