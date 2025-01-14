from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import time
import threading

from old.database.database_manager import DatabaseManager
from old.extractors.post_extractor import PostExtractor
from old.core.reddit_client import RedditClient
from old.utils.logger import logger
from old.models.database_models import ExtractionConfigDB


def run_in_thread(func, *args, **kwargs):
    """Executes a function in a separate thread."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread


class ExtractionScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.database_manager = DatabaseManager()
        self.reddit_client = RedditClient()
        self.reddit_instance = self.reddit_client.get_reddit_instance()
        self.post_extractor = PostExtractor(self.reddit_instance)
        self.job_interval = 5  # intervalo entre os jobs em segundos

    def start(self):
        """Starts the scheduler and adds existing jobs."""
        self._add_existing_jobs()
        self.scheduler.start()
        logger.info("Agendador de extração iniciado.")

    def _add_existing_jobs(self):
        """Adds all enabled extraction configurations as jobs."""
        session = self.database_manager.Session()
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
            #TODO: implementar agendamento por intervalo
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
                for _ in self.post_extractor.extract_posts_from_subreddit(
                    config.subreddit_name,
                    config.sort_criteria,
                    config.batch_size,
                    config.days_ago,
                    config.limit
                ):
                    pass
            elif config.type == "search":
                for _ in self.post_extractor.extract_posts_from_search(
                    config.query,
                    config.sort_criteria,
                    config.batch_size,
                    config.days_ago,
                    config.limit
                ):
                    pass
            self.database_manager.update_extraction_config(config.id)
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