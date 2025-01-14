from unittest.mock import patch
import pytest
from src.adapters.extraction_scheduler import ExtractionScheduler
from src.adapters.database_adapter import DatabaseAdapter
import time


@pytest.fixture
def mock_database_adapter():
    """Fixture para criar um mock do DatabaseGateway."""
    mock_adapter = DatabaseAdapter()
    return mock_adapter


def test_extraction_scheduler_start_and_run(mock_database_adapter):
    """Testa se o scheduler inicia e executa corretamente a extração."""
    config = {
        "type": "subreddit",
        "subreddit_name": "SaaS",
        "sort_criteria": "hot",
        "batch_size": 10,
        "days_ago": 1,
        "limit": 10,
        "schedule_time": "00:10",  # Horario da extração
        "daily": True,
        "enabled": True
    }
    mock_database_adapter.add_extraction_config(config)
    extraction_scheduler = ExtractionScheduler()

    with patch.object(extraction_scheduler, '_execute_extraction') as mock_execute_extraction:
        extraction_scheduler.start()
        time.sleep(2)
        extraction_scheduler.shutdown()
        assert mock_execute_extraction.call_count >= 1


def test_extraction_scheduler_run_now(mock_database_adapter):
    """Testa a execução imediata da extração."""
    config = {
        "type": "subreddit",
        "subreddit_name": "SaaS",
        "sort_criteria": "hot",
        "batch_size": 10,
        "days_ago": 1,
        "limit": 10,
        "schedule_time": "00:10",  # Horario da extração
        "daily": True,
        "enabled": True
    }
    mock_database_adapter.add_extraction_config(config)
    extraction_scheduler = ExtractionScheduler()

    with patch.object(extraction_scheduler, '_execute_extraction') as mock_execute_extraction:

        configs = mock_database_adapter.get_all_extraction_configs()
        for config in configs:
            if config.get("subreddit_name") == "SaaS":
                extraction_scheduler.run_extraction_now(config)
        time.sleep(2)
        assert mock_execute_extraction.call_count >= 1
        extraction_scheduler.shutdown()