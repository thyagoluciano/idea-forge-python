# src/adapters/analysis_scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import threading

from src.adapters.database_adapter import DatabaseAdapter
from src.adapters.gemini_adapter import GeminiAdapter
from src.core.use_cases.analysis_use_case import AnalysisUseCase
from src.core.utils.logger import setup_logger

logger = setup_logger(__name__)


def run_in_thread(func, *args, **kwargs):
    """Executes a function in a separate thread."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread


class AnalysisScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.database_adapter = DatabaseAdapter()
        self.gemini_adapter = GeminiAdapter()
        self.analysis_use_case = AnalysisUseCase(self.gemini_adapter, self.database_adapter)
        self.job_interval = 10  # intervalo entre os jobs em segundos
        self.batch_size = 10

    def start(self):
        """Starts the scheduler and adds existing jobs."""
        self._add_existing_jobs()
        self.scheduler.start()
        logger.info("Agendador de análise iniciado.")

    def _add_existing_jobs(self):
        """Adds all enabled analysis configurations as jobs."""
        # Por enquanto vamos adicionar apenas um job fixo
        self._add_job()

    def _add_job(self):
        """Adds a single job to the scheduler."""
        trigger = CronTrigger(minute="0")  # execute a cada hora
        self.scheduler.add_job(
            self._run_analysis,
            trigger=trigger,
            id="analysis_job",
            name=f"Analysis Job"
        )
        logger.info(f"Agendamento para análise adicionado")

    def _run_analysis(self):
        """Runs the analysis."""
        run_in_thread(self._execute_analysis)

    def _execute_analysis(self):
        """Executes the analysis and handle the interval."""
        logger.info("Iniciando análise dos posts.")
        try:
            self.analysis_use_case.analyze_posts(self.batch_size)
            logger.info("Análise dos posts finalizada com sucesso.")
        except Exception as e:
            logger.error(f"Erro durante a execução da análise dos posts: {e}")
        finally:
            time.sleep(self.job_interval)

    def run_analysis_now(self):
        """Runs the analysis immediately."""
        logger.info("Executando análise manualmente.")
        run_in_thread(self._execute_analysis)

    def shutdown(self):
        """Shuts down the scheduler."""
        self.scheduler.shutdown()
        logger.info("Agendador de análise finalizado.")