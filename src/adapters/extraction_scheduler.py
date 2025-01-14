from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import threading

from src.adapters.database_adapter import DatabaseAdapter
from src.core.use_cases.extraction_use_case import ExtractionUseCase
from src.adapters.reddit_adapter import RedditAdapter
from src.database.models.database_models import ExtractionConfigDB
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


def run_in_thread(func, *args, **kwargs):
    """Executes a function in a separate thread."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread


class ExtractionScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.database_adapter = DatabaseAdapter()
        self.reddit_adapter = RedditAdapter()
        self.extraction_use_case = ExtractionUseCase(self.reddit_adapter, self.database_adapter)
        self.job_interval = 5  # intervalo entre os jobs em segundos

    def start(self):
        """Starts the scheduler and adds existing jobs."""
        self._add_existing_jobs()
        self.scheduler.start()
        logger.info("Agendador de extração iniciado.")

    def _add_existing_jobs(self):
        """Adds all enabled extraction configurations as jobs."""
        session = self.database_adapter.Session()
        try:
            configs = session.query(ExtractionConfigDB).filter(ExtractionConfigDB.enabled == True).all()
            for config in configs:
                self._add_job(config)
        except Exception as e:
            logger.error(f"Erro ao buscar subreddits no banco de dados: {e}")
        finally:
            session.close()

    def _add_job(self, config):
        """Adds a single job to the scheduler."""
        if config.daily and config.schedule_time:
            trigger = CronTrigger(hour=config.schedule_time.split(":")[0], minute=config.schedule_time.split(":")[1])
        else:
            # TODO: implementar agendamento por intervalo
            raise ValueError("Agendamento por intervalo não implementado")
        self.scheduler.add_job(
            self._run_extraction,
            trigger=trigger,
            args=[config],
            id=str(config.id),
            name=f"Extraction Job {config.id}"
        )
        logger.info(f"Agendamento para extração com ID {config.id} adicionado")

    def _run_extraction(self, config):
        """Runs the extraction based on the config."""
        run_in_thread(self._execute_extraction, config)

    def _execute_extraction(self, config):
        """Executes the extraction and handle the interval."""
        logger.info(f"Iniciando extração com ID {config.id}")
        try:
            if config.type == "subreddit":
                 self.extraction_use_case.extract_posts_from_subreddit(
                     config.subreddit_name,
                     config.sort_criteria,
                     config.batch_size,
                     config.days_ago,
                     config.limit
                 )

            elif config.type == "search":
                 self.extraction_use_case.extract_posts_from_search(
                    config.query,
                    config.sort_criteria,
                    config.batch_size,
                    config.days_ago,
                    config.limit
                 )
            self.database_adapter.update_extraction_config(config.id)
            logger.info(f"Extração com ID {config.id} finalizada com sucesso.")
        except Exception as e:
            logger.error(f"Erro durante a execução da extração com ID {config.id}: {e}")
        finally:
            time.sleep(self.job_interval)

    def run_extraction_now(self, config):
        """Runs the extraction immediately."""
        logger.info(f"Executando extração manualmente com ID {config.id}")
        run_in_thread(self._execute_extraction, config)

    def shutdown(self):
        """Shuts down the scheduler."""
        self.scheduler.shutdown()
        logger.info("Agendador de extração finalizado.")