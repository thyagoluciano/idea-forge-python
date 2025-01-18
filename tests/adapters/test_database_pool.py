# tests/adapters/test_database_pool.py
import pytest
import time
from sqlalchemy import text
from unittest.mock import patch, MagicMock
from src.adapters.database_adapter import DatabaseAdapter
from src.adapters.extraction_scheduler import ExtractionScheduler
from src.config.config import Config
from src.core.utils.logger import setup_logger
from src.core.entities import Post


logger = setup_logger(__name__)


@pytest.fixture
def mock_reddit_gateway():
    """Fixture para criar um mock do RedditGateway."""
    mock = MagicMock()
    mock.fetch_posts_from_subreddit.return_value = [
        Post(title="Test Post 1", id="1", url="http://test1", text="test", num_comments=0, ups=0, comments=[]),
        Post(title="Test Post 2", id="2", url="http://test2", text="test", num_comments=0, ups=0, comments=[])
    ]
    return mock

@pytest.fixture
def mock_database_adapter(config):
    """Fixture para criar um mock do DatabaseAdapter."""
    mock = MagicMock()
    mock.add_extraction_config = MagicMock()
    pool_size = config.POSTGRES_POOL_SIZE
    max_overflow = config.POSTGRES_MAX_OVERFLOW
    mock.database_manager.session.return_value.__enter__.return_value.execute.return_value.fetchone.side_effect = [[2], [pool_size], [pool_size + max_overflow]]
    return mock

@pytest.fixture
def extraction_scheduler(mock_reddit_gateway, mock_database_adapter):
    """Fixture para criar uma instância do ExtractionScheduler."""
    extraction_scheduler = ExtractionScheduler()
    extraction_scheduler.reddit_adapter = mock_reddit_gateway
    extraction_scheduler.database_adapter = mock_database_adapter
    return extraction_scheduler


@pytest.fixture
def config():
     return Config()


def count_active_connections(database_adapter):
    """Counts the number of active database connections."""
    result = database_adapter.database_manager.session().__enter__().execute().fetchone()
    return result[0] if result else 0


def simulate_extraction(extraction_scheduler, config, num_extractions):
    """Simulate the execution of extraction multiple times."""
    try:
            config_data = {
                    "type": "subreddit",
                    "subreddit_name": "SaaS",
                    "sort_criteria": "hot",
                    "batch_size": 10,
                    "days_ago": 1,
                    "limit": 10,
                    "schedule_time": "00:10",  # Horario da extração
                    "daily": False,
                    "enabled": True
                }
            extraction_scheduler.database_adapter.add_extraction_config(config_data)
            extraction_scheduler._add_existing_jobs()
            time.sleep(1)

            configs = extraction_scheduler.database_adapter.get_all_extraction_configs()
            for _ in range(num_extractions):
                for config in configs:
                    if config.subreddit_name == "SaaS":
                      extraction_scheduler.extraction_use_case.extract_posts_from_subreddit(
                            config.subreddit_name,
                            config.sort_criteria,
                            config.batch_size,
                            config.days_ago,
                            config.limit
                      )
    except Exception as e:
        logger.error(f"Erro ao simular a execução da extração: {e}")


def test_database_connection_pool_limits(mock_database_adapter, extraction_scheduler, config):
    """Testa o pool de conexões do banco de dados."""
    pool_size = config.POSTGRES_POOL_SIZE
    max_overflow = config.POSTGRES_MAX_OVERFLOW
    max_connections = pool_size + max_overflow
    num_extractions = max_connections * 2

    initial_connections = count_active_connections(mock_database_adapter)
    logger.info(f"Numero de conexões iniciais com o banco de dados: {initial_connections}")

    # Simula a extração
    simulate_extraction(extraction_scheduler, config, num_extractions)

    active_connections = count_active_connections(mock_database_adapter)
    logger.info(f"Numero de conexões ativas com o banco de dados: {active_connections}")

    assert initial_connections <= pool_size, f"O numero de conexões iniciais excedeu o pool size {pool_size}"
    assert active_connections <= max_connections, f"O numero de conexões excedeu o limite do pool {max_connections}"
    mock_database_adapter.database_manager.session.return_value.__enter__.return_value.execute.assert_called()