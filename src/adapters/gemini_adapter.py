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

logger = setup_logger(__name__)


class GeminiAdapter(GeminiGateway):
    def __init__(self):
        self.config = Config()
        try:
            genai.configure(api_key=self.config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(self.config.GEMINI_MODEL)
            logger.info("Conexão com Gemini estabelecida com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao conectar com o Gemini: {e}")
            self.model = None
        self.semaphore = threading.Semaphore(1)  # Limita para 1 thread por vez
        self.retry_delay = int(os.getenv("GEMINI_RETRY_DELAY", 20))  # Tempo de espera entre as tentativas em segundos
        self.max_retries = 3  # Número máximo de tentativas

    def _build_prompt(self, text: str, post_title: str) -> str:
        """Builds the prompt for the Gemini API."""
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
            4.  For each identified SaaS product, categorize it in one of the following categories:
                - Project Management
                - Customer Relationship Management
                - Marketing and Sales Automation
                - Finance Management
                - Human Resources Management
                - E-commerce and Retail
                - Education and Training
                - Data Analytics and Business Intelligence
                - Health and Wellness
                - Social Media Management
                - Productivity and Workflow
                - Collaboration and Communication
                - IT and Security Management
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
                                    "category": "Category of the SaaS product"
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
                                    "category": "Categoria do produto SaaS"
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
        """Calls the Gemini API with retry logic."""
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
                logger.error(f"Erro ao analisar com Gemini: {e}")
                if "429 Resource has been exhausted" in str(e):
                    retries += 1
                    logger.warning(
                        f"Erro de quota do Gemini, tentando novamente em {self.retry_delay} segundos (tentativa {retries}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                else:
                    return None
        return None

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
