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
        Analisa um texto usando a API do Google Gemini.

        Args:
          text: texto a ser analisado
        Returns:
           Um dicionário contendo o title, description, category e score.
        """
        if not self.model:
            logger.error("Modelo Gemini não está inicializado.")
            return {"title": "", "description": "", "category": "", "score": ""}

        prompt = f"""
        Você é um assistente especializado em análise de conteúdos para identificar oportunidades de desenvolvimento de produtos SaaS. Sua tarefa é analisar um objeto JSON que inclui title, text, e comments de uma postagem, e gerar insights sobre dores, problemas, e soluções relatadas. Com base nessas informações, você deve:

        Identificar Problemas: Analise o title, text e comments para listar problemas ou desafios mencionados.
        Extrair Soluções: Identifique quaisquer soluções ou ideias propostas que possam ser transformadas em produtos SaaS.
        Gerar Produtos SaaS:
        Crie um nome cativante para cada oportunidade de produto SaaS.
        Descreva como o produto resolveria o problema, incluindo features e diferenciais principais.
        Avaliar Viabilidade:
        Atribua um score de facilidade de implementação de 1 a 5.
        Atribua um score de viabilidade de mercado de 1 a 100.
        Estruturar Saída:
        Retorne as informações em um formato estruturado, como um dicionário JSON.
        Aqui está o objeto JSON a ser analisado:
        {text}
        Certifique-se de que a saída seja clara e bem organizada, destacando múltiplas oportunidades se identificadas dentro das informações fornecidas.
        """
        # prompt = f"""
        # Analise o texto a seguir e me retorne um objeto json com: title, description, category e um score de 1 a 10 para a ideia.
        # Se o texto nao tiver um potencial de ideia de software como serviço retorne um objeto json com esses valores vazios.
        # texto:
        # {text}
        # """
        try:
            response = self.model.generate_content(prompt)
            json_str = response.text.replace("```json", "").replace("```", "")
            return json.loads(json_str)
        except json.JSONDecodeError as e:
             logger.error(f"Erro ao decodificar resposta JSON do Gemini: {e}")
             return {"title": "", "description": "", "category": "", "score": ""}
        except Exception as e:
           logger.error(f"Erro ao analisar com Gemini: {e}")
           return {"title": "", "description": "", "category": "", "score": ""}