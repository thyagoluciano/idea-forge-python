import json
import os
from models.idea import Idea
from utils.logger import logger
import json


class IdeaDatabase:
    def __init__(self, db_file="ideas.json"):
        self.db_file = db_file
        self.ideas = self._load_database()

    def _load_database(self):
        """Carrega as ideias do arquivo JSON."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    return [Idea(**item) for item in data]
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Erro ao carregar o banco de dados: {e}")
                return []

        return []

    def _save_database(self):
        """Salva as ideias no arquivo JSON."""
        try:
            with open(self.db_file, 'w') as f:
                data = [idea.to_dict() for idea in self.ideas]
                json.dump(data, f, indent=2)
                logger.info("Banco de dados salvo com sucesso.")
        except IOError as e:
            logger.error(f"Erro ao salvar o banco de dados: {e}")

    def add_idea(self, idea):
        """Adiciona uma nova ideia ao banco de dados."""
        if self.is_duplicate(idea):
            logger.warning(f"A ideia com ID {idea.reddit_content_id} já existe no banco de dados.")
            return False
        self.ideas.append(idea)
        self._save_database()
        logger.info(f"Ideia '{idea.product_name}' adicionada ao banco de dados.")
        return True

    def is_duplicate(self, idea):
        """Verifica se existe uma ideia com o mesmo reddit_content_id"""
        return any(f"{i.reddit_content_id}_{i.product_name}" == f"{idea.reddit_content_id}_{idea.product_name}" for i in self.ideas)

    def get_all_ideas(self):
        """Retorna todas as ideias do banco de dados."""
        return self.ideas