import google.generativeai as genai
import json
from config.config import Config
from utils.logger import logger


class GeminiAPI:
    def __init__(self):
        self.config = Config()
        try:
            genai.configure(api_key=self.config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(self.config.GEMINI_MODEL)
            logger.info("Conexão com Gemini estabelecida com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao conectar com o Gemini: {e}")
            self.model = None

    def analyze_with_gemini(self, text):
        """
        Analisa um texto usando a API do Google Gemini, garantindo um formato de resposta JSON consistente.

        Args:
          text: texto a ser analisado
        Returns:
           Um dicionário contendo o title, description, category e score.
        """
        if not self.model:
            logger.error("Modelo Gemini não está inicializado.")
            return {"post_analysis": {"insights": [], "post_description": "", "post_title": ""}}

        prompt = f"""
        Você é um assistente especializado em análise de conteúdos para identificar oportunidades de desenvolvimento de produtos SaaS. Sua tarefa é analisar o texto de um post e seus comentários, e gerar insights sobre dores, problemas e soluções relatadas, formatando a resposta em um JSON específico.

        Instruções:

        1.  Analise o texto para identificar problemas ou desafios mencionados.
        2.  Identifique quaisquer soluções ou ideias propostas que possam ser transformadas em produtos SaaS.
        3.  Para cada oportunidade de produto SaaS identificada:
            *   Crie um nome cativante para o produto.
            *   Descreva como o produto resolveria o problema.
            *   Liste os principais diferenciais.
            *   Liste as principais features.
            *   Atribua um score de facilidade de implementação (1 a 5).
            *   Atribua um score de viabilidade de mercado (1 a 100).
        4.  Formate a saída como um JSON seguindo a seguinte estrutura:

        {{
            "post_analysis": {{
                "insights": [
                    {{
                        "problem": "Problema identificado no texto",
                        "saas_product": {{
                            "description": "Descrição do produto SaaS",
                            "differentiators": ["Diferencial 1", "Diferencial 2", ...],
                            "features": ["Feature 1", "Feature 2", ...],
                            "implementation_score": int,
                            "market_viability_score": int,
                            "name": "Nome do Produto SaaS"
                        }},
                        "solution": "Solução proposta"
                    }},
                   ... (Mais oportunidades, se encontradas)
                ],
                "post_description": "Descrição geral do post",
                "post_title": "Título do post"
            }}
        }}

        5. Se não encontrar nenhuma ideia, retorne a estrutura com insights vazios:
          {{
            "post_analysis": {{
                "insights": [],
                "post_description": "",
                "post_title": ""
            }}
          }}


        Aqui está o texto a ser analisado:
        {text}

        Respeite RIGOROSAMENTE a estrutura do JSON, sem adicionar nenhum campo extra e sem remover nenhum campo obrigatório.
        """
        try:
            response = self.model.generate_content(prompt)
            json_str = response.text.replace("```json", "").replace("```", "")
            response_json = json.loads(json_str)

            if not response_json.get("post_analysis") or not isinstance(response_json.get("post_analysis").get("insights"),list):
                 logger.warning("Formato da resposta do Gemini está incorreta, retornando insights vazios")
                 return {"post_analysis": {"insights": [], "post_description": "", "post_title": ""}}

            return response_json
        except json.JSONDecodeError as e:
             logger.error(f"Erro ao decodificar resposta JSON do Gemini: {e}")
             return {"post_analysis": {"insights": [], "post_description": "", "post_title": ""}}
        except Exception as e:
           logger.error(f"Erro ao analisar com Gemini: {e}")
           return {"post_analysis": {"insights": [], "post_description": "", "post_title": ""}}