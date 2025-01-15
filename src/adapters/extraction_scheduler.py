from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import time
from concurrent.futures import ThreadPoolExecutor


from src.adapters.database_adapter import DatabaseAdapter
from src.core.use_cases.extraction_use_case import ExtractionUseCase
from src.adapters.reddit_adapter import RedditAdapter
from src.database.models.database_models import ExtractionConfigDB
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


class ExtractionScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.database_adapter = DatabaseAdapter()
        self.reddit_adapter = RedditAdapter()
        self.extraction_use_case = ExtractionUseCase(self.reddit_adapter, self.database_adapter)
        self.job_interval = 5  # intervalo entre os jobs em segundos
        self.executor = ThreadPoolExecutor(max_workers=5)

    def start(self):
        """Starts the scheduler and adds existing jobs."""
        self._add_existing_jobs()
        self.scheduler.start()
        logger.info("Agendador de extração iniciado.")

    def _add_existing_jobs(self):
        """Adds all enabled extraction configurations as jobs."""
        try:
            with self.database_adapter.database_manager.session() as session:
                configs = session.query(ExtractionConfigDB).filter(ExtractionConfigDB.enabled == True).all()
                for config in configs:
                    self._add_job(config)
        except Exception as e:
            logger.error(f"Erro ao buscar configurações no banco de dados: {e}")

    def _add_job(self, config):
        """Adds a single job to the scheduler."""
        job_id = str(config.id)
        job_name = f"Extraction Job {config.id}"
        if config.daily and config.schedule_time:
            trigger = CronTrigger(hour=config.schedule_time.split(":")[0], minute=config.schedule_time.split(":")[1])
            logger.info(f"Agendamento para extração com ID {job_id} adicionado, usando CronTrigger.")
        elif not config.daily and config.schedule_time:
             trigger = IntervalTrigger(minutes=int(config.schedule_time), start_date=config.last_run)
             logger.info(f"Agendamento para extração com ID {job_id} adicionado, usando IntervalTrigger.")
        else:
            raise ValueError(f"Agendamento invalido para extração com ID {config.id}")

        self.scheduler.add_job(
            self._run_extraction,
            trigger=trigger,
            args=[config],
            id=job_id,
            name=job_name
        )
        logger.info(f"Agendamento para extração com ID {config.id} adicionado")

    def _run_extraction(self, config):
        """Runs the extraction based on the config."""
        job_id = str(config.id)
        job_name = f"Extraction Job {config.id}"
        logger.info(f"Iniciando execução da extração com ID {job_id}")
        self.executor.submit(self._execute_extraction, config)

    def _execute_extraction(self, config):
        """Executes the extraction and handle the interval."""
        job_id = str(config.id)
        job_name = f"Extraction Job {config.id}"
        start_time = time.time()
        logger.info(f"Executando extração com ID {job_id} - Iniciou às {start_time}")
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
            logger.info(f"Extração com ID {job_id} finalizada com sucesso.")

        except Exception as e:
             logger.error(f"Erro durante a execução da extração com ID {job_id}: {e}", exc_info=True)
        finally:
             end_time = time.time()
             execution_time = end_time - start_time
             logger.info(f"Extração com ID {job_id} finalizada - Tempo de execução: {execution_time:.2f} segundos.")
             time.sleep(self.job_interval)

    def run_extraction_now(self, config):
        """Runs the extraction immediately."""
        job_id = str(config.id)
        logger.info(f"Executando extração manualmente com ID {job_id}")
        self.executor.submit(self._execute_extraction, config)

    def shutdown(self):
        """Shuts down the scheduler."""
        self.scheduler.shutdown()
        logger.info("Agendador de extração finalizado.")