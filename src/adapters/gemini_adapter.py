# src/adapters/gemini_adapter.py
import os

import google.generativeai as genai
import json
import threading
import time
from typing import Dict, Optional
import re

from src.config.config import Config
from src.core.ports.gemini_gateway import GeminiGateway
from src.core.utils.logger import setup_logger
from src.adapters.database_adapter import DatabaseAdapter
from src.database.models.category_db import CategoryDB

logger = setup_logger(__name__)


class GeminiAdapter(GeminiGateway):
    def __init__(self):
        self.config = Config()
        self.api_keys = self.config.google_api_keys
        self.current_key_index = 0
        self._configure_gemini()
        self.semaphore = threading.Semaphore(1)  # Limita para 1 thread por vez
        self.retry_delay = int(os.getenv("GEMINI_RETRY_DELAY", 20))  # Tempo de espera entre as tentativas em segundos
        self.max_retries = 3  # Número máximo de tentativas
        self.database_adapter = DatabaseAdapter()

    def _configure_gemini(self):
        """Configures the Gemini API client with the current API key."""
        try:
            genai.configure(api_key=self.api_keys[self.current_key_index])
            self.model = genai.GenerativeModel(self.config.GEMINI_MODEL)
            logger.info(f"Conexão com Gemini estabelecida com sucesso usando chave {self.current_key_index}.")
        except Exception as e:
            logger.error(f"Erro ao conectar com o Gemini usando chave {self.current_key_index}: {e}")
            self.model = None

    def _build_prompt(self, text: str, post_title: str) -> str:
        """Builds the prompt for the Gemini API."""

        with self.database_adapter.database_manager.session() as session:
            categories = session.query(CategoryDB).all()
            categories_str = "\n".join(
                [f"| {category.id} | {category.category_en} | {category.category_pt} |" for category in categories])

        return f"""
            You are an assistant specialized in content analysis to identify opportunities for the development of SaaS products. Your task is to analyze a post and its comments, generating insights about pains, problems, and solutions reported, and format the response into two JSON structures: one in English and one translated into Brazilian Portuguese.

            Instructions:

            1.  Analyze the text to identify problems or challenges mentioned.
            2.  Identify any proposed solutions or ideas that can be transformed into SaaS products.
            3.  For each SaaS product opportunity identified:
                *   Create a catchy name for the product.
                *   Describe in detail how the product would solve the problem, providing clear and comprehensive information so that the reader can fully understand the idea.
                *   List the main differentiators.
                *   List the main features.
                *   Assign an implementation ease score (1 to 5).
                *   Assign a market viability score (1 to 100).
            4.  For each identified SaaS product, categorize it using only one of the categories from the list below and return the category ID in the JSON payload. Use the following table with category IDs and names for both english and portuguese:

            | ID | English | Portuguese |
            {categories_str}

            5.  Format the output as two JSONs:

            {{
                "en": {{
                    "post_analysis": {{
                        "insights": [
                            {{
                                "problem": "Problem identified in the text",
                                "saas_product": {{
                                    "description": "Detailed description of how the SaaS product solves the problem, ensuring clarity and comprehensive understanding of the idea.",
                                    "differentiators": ["Differentiator 1", "Differentiator 2", ...],
                                    "features": ["Feature 1", "Feature 2", ...],
                                    "implementation_score": int,
                                    "market_viability_score": int,
                                    "name": "SaaS Product Name",
                                    "category_id": int
                                }},
                                "solution": "Proposed solution"
                            }},
                        ... (More opportunities, if found)
                        ],
                        "post_description": "General post description",
                        "post_title": "Post title"
                    }}
                }}

                ,"pt": {{
                    "post_analysis": {{
                        "insights": [
                            {{
                                "problem": "Problema identificado no texto",
                                "saas_product": {{
                                    "description": "Descrição detalhada de como o produto SaaS resolve o problema, garantindo clareza e compreensão completa da ideia.",
                                    "differentiators": ["Diferencial 1", "Diferencial 2", ...],
                                    "features": ["Funcionalidade 1", "Funcionalidade 2", ...],
                                    "implementation_score": int,
                                    "market_viability_score": int,
                                    "name": "Nome do Produto SaaS",
                                     "category_id": int
                                }},
                                "solution": "Solução proposta"
                            }},
                        ... (Mais oportunidades, se encontradas)
                        ],
                        "post_description": "Descrição geral da postagem",
                        "post_title": "Título da postagem"
                    }}
                }}
            }}

            6. If no idea is found, return the structures with empty insights in both languages:

           {{
                "en": {{
                    "post_analysis": {{
                        "insights": [],
                        "post_description": "",
                        "post_title": "Post title"
                    }}
                }},
                "pt": {{
                    "post_analysis": {{
                        "insights": [],
                        "post_description": "",
                        "post_title": "Título da postagem"
                    }}
                }}
            }}

            Here is the text to be analyzed:
            {text}

            Strictly adhere to the JSON structures, without adding any extra fields and without removing any mandatory fields.
        """

    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """Calls the Gemini API with retry logic and key rotation."""
        if not self.model:
            logger.error("Modelo Gemini não está inicializado.")
            return None

        retries = 0
        while retries < self.max_retries:
            try:
                with self.semaphore:
                    response = self.model.generate_content(prompt)
                    return response.text
            except Exception as e:
                if "429 Resource has been exhausted" in str(e):
                    retries += 1
                    logger.warning(
                        f"Erro de quota do Gemini, tentando novamente com a chave atual em {self.retry_delay} segundos (tentativa {retries}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                    if retries >= self.max_retries:
                        if self._rotate_api_key():
                            retries = 0
                            logger.info(f"Rotacionando API Key, nova chave: {self.current_key_index}")
                            continue
                        else:
                            logger.error(f"Todas as chaves API foram usadas.")
                            return None

                else:
                    logger.error(f"Erro ao analisar com Gemini: {e}")
                    return None
        return None

    def _rotate_api_key(self) -> bool:
        """Rotates to the next API key in the list. Returns True if successful, False otherwise."""
        if not self.api_keys:
            return False
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self._configure_gemini()
        return True

    def _process_gemini_response(self, response_text: Optional[str], post_title: str) -> Dict:
        """Processes the response from the Gemini API."""
        if not response_text:
            return {"en": {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}},
                    "pt": {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}}
        try:
            json_str = response_text.replace("```json", "").replace("```", "")
            response_json = json.loads(json_str)

            if not response_json.get("en") or not response_json.get("pt"):
                logger.warning("Formato da resposta do Gemini está incorreta, retornando insights vazios")
                return {"en": {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}},
                        "pt": {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}}

            return response_json

        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar resposta JSON do Gemini: {e}")
            return {"en": {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}},
                    "pt": {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}}
        except Exception as e:
            logger.error(f"Erro inesperado ao processar resposta do Gemini: {e}")
            return {"en": {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}},
                    "pt": {"post_analysis": {"insights": [], "post_description": "", "post_title": post_title}}}

    def analyze_text(self, text: str, post_title: str) -> Optional[Dict]:
        """
        Analisa um texto usando a API do Google Gemini, garantindo um formato de resposta JSON consistente.
        """
        prompt = self._build_prompt(text, post_title)
        response_text = self._call_gemini_api(prompt)
        return self._process_gemini_response(response_text, post_title)