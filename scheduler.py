from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
from utils.logger import logger
import os
import time


def run_extractor():
    """Executa o script extractor.py."""
    try:
        logger.info("Iniciando a execução do extractor.py...")
        extractor_path = os.path.abspath("extractor.py")
        subprocess.run(["python", extractor_path], check=True)
        logger.info("extractor.py executado com sucesso.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar o extractor.py: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado ao executar o extractor.py: {e}")


def run_analyzer():
    """Executa o script analyzer.py."""
    try:
         logger.info("Iniciando a execução do analyzer.py...")
         analyzer_path = os.path.abspath("analyzer.py")
         subprocess.run(["python", analyzer_path], check=True)
         logger.info("analyzer.py executado com sucesso.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar o analyzer.py: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado ao executar o analyzer.py: {e}")


if __name__ == "__main__":
    # scheduler = BlockingScheduler()
    # # Agendamento do extractor.py para rodar toda semana (segunda-feira às 00:00)
    # scheduler.add_job(run_extractor, 'cron', day_of_week='mon', hour=0, minute=0)
    # # Agendamento do analyzer.py para rodar diariamente às 04:00
    # scheduler.add_job(run_analyzer, 'cron', hour=4, minute=0)

    # logger.info("Agendador inicializado. Aguardando a execução dos jobs...")
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     logger.info("Agendador finalizado.")
    run_extractor()
    # run_analyzer()
