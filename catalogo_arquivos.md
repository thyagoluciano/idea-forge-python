# Diretórios Ignorados

- `/Users/thyagoluciano/Developer/projetos/idea-forge/venv`
- `/Users/thyagoluciano/Developer/projetos/idea-forge/.idea`
- `/Users/thyagoluciano/Developer/projetos/idea-forge/.git`
- `/Users/thyagoluciano/Developer/projetos/idea-forge/sample`

# Arquivos Ignorados

- `*.pyc`
- `.DS_Store`
- `*.logcode_2_md.py.gitignore`

---

## requirements.txt

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/requirements.txt`

```txt
praw
python-dotenv
google-generativeai
```

## ideas.json

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/ideas.json`

```json
[
  {
    "reddit_content_id": "1hrqg5q",
    "product_name": "PushPro Engage",
    "problem": "Businesses struggle to effectively reach their audience with important updates and content, facing low engagement on social media and email.",
    "solution_description": "PushPro Engage is a SaaS platform that enables businesses to send push notifications directly to their audience\"s phones, ensuring immediate attention and high engagement rates. It bypasses the limitations of social media algorithms and the low open rates of email newsletters. The platform offers customizable notifications, user segmentation and detailed analytics, providing a comprehensive solution for audience engagement.",
    "implementation_score": 3,
    "market_viability_score": 75,
    "differentials": [
      "High engagement rates compared to email and social media",
      "Guaranteed delivery",
      "Ability to segment and target users effectively",
      "Real-time analytics dashboard to track performance"
    ],
    "features": [
      "Customizable push notifications",
      "User segmentation",
      "Real-time analytics",
      "Scheduled notifications",
      "Integration with other marketing tools"
    ]
  },
  {
    "reddit_content_id": "1hrqg5q",
    "product_name": "TabWise AI",
    "problem": "Users often need to extract information or interact with the content of websites they are currently browsing, lacking a seamless way to do so.",
    "solution_description": "TabWise AI is a browser extension that lets users interact directly with any open web page using AI. It allows users to summarize, extract data, and engage in contextual conversations with the current webpage, simplifying workflows and boosting productivity.  The extension uses a large language model for advanced features, ensuring accurate and efficient results.",
    "implementation_score": 4,
    "market_viability_score": 80,
    "differentials": [
      "Direct interaction with live webpages, not just pre-set knowledge",
      "Ability to extract and export data from tables and unstructured content",
      "Context awareness for better assistance and summaries",
      "Integration with a cutting-edge large language model (LLM)"
    ],
    "features": [
      "Chat with any tab",
      "Data extraction (CSV/JSON)",
      "Article summarization",
      "Context-aware assistance",
      "Integration with a large language model (LLM)"
    ]
  },
  {
    "reddit_content_id": "1hrqg5q",
    "product_name": "IdeaSpark",
    "problem": "Business owners are seeking new business opportunities that are not capital intensive.",
    "solution_description": "IdeaSpark is a SaaS platform for generating, validating, and refining business ideas that require low initial capital. The platform uses user-input data, market trends and AI to generate and validate ideas. It helps users discover opportunities in specific industries or niches, assess their feasibility and create basic business models. It aims to be a catalyst for entrepreneurial thinking by providing a structured approach to idea generation and validation.",
    "implementation_score": 2,
    "market_viability_score": 60,
    "differentials": [
      "Focus on low-capital business models",
      "User-driven insights and community feedback",
      "Integration with market analysis tools for real-time data",
      "AI-powered idea validation that goes beyond superficial analysis"
    ],
    "features": [
      "AI-powered idea generation",
      "Market validation tools",
      "Low-capital business model templates",
      "User-driven feedback system",
      "Opportunity assessment reports"
    ]
  },
  {
    "reddit_content_id": "1hrqg5q",
    "product_name": "DirectoryEase",
    "problem": "Businesses and entrepreneurs need an easy way to build online directories without coding",
    "solution_description": "DirectoryEase is a no-code SaaS platform designed to enable anyone to create their online directory without needing to write a single line of code. It offers a wide variety of customizable templates, intuitive drag-and-drop editors and a suite of features to manage listings, users, and content. It\"s ideal for small businesses, community groups, and entrepreneurs who want to launch a directory quickly and affordably.",
    "implementation_score": 3,
    "market_viability_score": 85,
    "differentials": [
      "Intuitive no-code interface suitable for non-technical users",
      "Highly customizable and feature-rich directory templates",
      "Simplified user onboarding and directory management",
      "Affordable pricing tiers for different needs",
      "Integrations for monetization (payment gateways, advertisement)"
    ],
    "features": [
      "Drag and drop directory builder",
      "Customizable directory templates",
      "User and listing management",
      "Search and filter functionalities",
      "Integration with payment gateways"
    ]
  }
]
```

## catalogo_arquivos.md

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/catalogo_arquivos.md`

```md

```

## cli.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/cli.py`

```py
import json

from core.reddit_api import RedditAPI
from core.gemini_api import GeminiAPI
from models.idea import Idea
from database.database import IdeaDatabase
from utils.logger import logger
from config.config import Config


def main():
    Config()
    reddit_api = RedditAPI()
    gemini_api = GeminiAPI()
    idea_db = IdeaDatabase()

    if not reddit_api.reddit:
        logger.error("Não foi possível iniciar a aplicação pois não foi estabelecida a conexão com a API do Reddit")
        return

    if not gemini_api.model:
        logger.error("Não foi possível iniciar a aplicação pois não foi estabelecida a conexão com a API do Gemini")
        return

    # Obtém posts e comentários do Reddit
    posts_data = reddit_api.get_posts_and_comments()

    for post in posts_data:
        full_text = f"Post: {post['title']}\n{post['text']}\n"
        logger.info(f"Analisando o post: {post['title']} ({post['id']})")
        logger.info(f"Upvotes: {post['upvotes']}, Número de comentários: {post['num_comments']}")
        for comment in post['comments']:
            full_text += f"Comment: {comment['text']}\n"
            logger.info(f"  - {comment['author']}: {comment['text'][:50]}... (Upvotes: {comment['upvotes']})")

        # Analisa o texto usando a API do Gemini
        analysis_result = gemini_api.analyze_with_gemini(full_text)

        if analysis_result and analysis_result.get("post_analysis").get("insights"):
            analysis_result_list = analysis_result.get("post_analysis").get("insights")
            for result in analysis_result_list:
                idea = Idea(
                    reddit_content_id=post['id'],
                    product_name=result.get("saas_product").get('name'),
                    problem=result.get('problem'),
                    solution_description=result.get("saas_product").get('description'),
                    implementation_score=result.get("saas_product").get('implementation_score'),
                    market_viability_score=result.get("saas_product").get('market_viability_score'),
                    differentials=result.get("saas_product").get('differentiators'),
                    features=result.get("saas_product").get('features'),
                )
                if idea_db.add_idea(idea):
                    logger.info(f"Ideia adicionada: {idea}")
                    print(f"Ideia adicionada com sucesso: {idea.product_name}")
                else:
                    logger.warning(f"Não foi possível adicionar a ideia, pois ela já existe na base")
                    print(f"Ideia com ID {idea.reddit_content_id} já existe.")
        else:
            logger.warning(f"Não foi encontrada uma ideia para o post: {post['title']}")

    print("\nExtração e análise concluída!")

    for idea in idea_db.get_all_ideas():
        print(f"Ideia: {idea}")


if __name__ == "__main__":
    main()
```

## code_2_md.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/code_2_md.py`

```py
import os
import pathlib
from typing import List


def should_ignore_path(path: str, ignore_dirs: List[str], ignore_files: List[str]) -> bool:
    """
    Verifica se um caminho deve ser ignorado.

    Args:
        path (str): Caminho a ser verificado
        ignore_dirs (List[str]): Lista de diretórios a serem ignorados
        ignore_files (List[str]): Lista de arquivos a serem ignorados

    Returns:
        bool: True se o caminho deve ser ignorado, False caso contrário
    """
    normalized_path = os.path.normpath(path)

    # Verifica se o caminho está em um diretório ignorado
    for ignore_dir in ignore_dirs:
        normalized_ignore = os.path.normpath(ignore_dir)
        if normalized_path.startswith(normalized_ignore):
            return True

    # Verifica se o arquivo deve ser ignorado
    file_name = os.path.basename(path)
    for ignore_pattern in ignore_files:
        # Permite wildcards simples (*.extensão)
        if ignore_pattern.startswith('*'):
            if file_name.endswith(ignore_pattern[1:]):
                return True
        # Comparação exata do nome do arquivo
        elif file_name == ignore_pattern:
            return True

    return False


def directory_to_markdown(directory_path: str, ignore_dirs: List[str] = None, ignore_files: List[str] = None):
    """
    Converte todos os arquivos de um diretório para um arquivo Markdown,
    ignorando diretórios e arquivos especificados.

    Args:
        directory_path (str): Caminho do diretório a ser processado
        ignore_dirs (List[str], optional): Lista de diretórios a serem ignorados
        ignore_files (List[str], optional): Lista de arquivos a serem ignorados
    """
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []

    # Normaliza os caminhos dos diretórios a serem ignorados
    ignore_dirs = [os.path.join(directory_path, d) if not os.path.isabs(d) else d
                   for d in ignore_dirs]

    # Verifica se o diretório existe
    if not os.path.exists(directory_path):
        print(f"Diretório {directory_path} não encontrado.")
        return

    # Cria o arquivo Markdown de saída
    output_file = 'catalogo_arquivos.md'

    with open(output_file, 'w', encoding='utf-8') as markdown_file:
        # Adiciona informação sobre diretórios e arquivos ignorados
        if ignore_dirs or ignore_files:
            if ignore_dirs:
                markdown_file.write("# Diretórios Ignorados\n\n")
                for ignore_dir in ignore_dirs:
                    markdown_file.write(f"- `{ignore_dir}`\n")
                markdown_file.write("\n")

            if ignore_files:
                markdown_file.write("# Arquivos Ignorados\n\n")
                for ignore_file in ignore_files:
                    markdown_file.write(f"- `{ignore_file}`\n")
                markdown_file.write("\n")

            markdown_file.write("---\n\n")

        # Percorre todos os arquivos no diretório
        for root, dirs, files in os.walk(directory_path):
            # Remove diretórios que devem ser ignorados
            dirs[:] = [d for d in dirs if not should_ignore_path(
                os.path.join(root, d), ignore_dirs, ignore_files)]

            for file in files:
                file_path = os.path.join(root, file)

                # Pula arquivo se estiver em um diretório ignorado ou se for um arquivo ignorado
                if should_ignore_path(file_path, ignore_dirs, ignore_files):
                    continue

                # Obtém o caminho relativo
                relative_path = os.path.relpath(file_path, directory_path)

                # Determina o tipo de linguagem para syntax highlighting
                file_extension = pathlib.Path(file).suffix[1:]
                language = file_extension if file_extension else ''

                # Adiciona cabeçalho com path do arquivo
                markdown_file.write(f"## {relative_path}\n\n")
                markdown_file.write(f"**Caminho completo**: `{file_path}`\n\n")

                try:
                    # Tenta ler o conteúdo do arquivo
                    with open(file_path, 'r', encoding='utf-8') as current_file:
                        file_content = current_file.read()
                        markdown_file.write(f"```{language}\n{file_content}\n```\n\n")
                except UnicodeDecodeError:
                    # Para arquivos binários
                    markdown_file.write("**[Arquivo binário - não foi possível exibir conteúdo]**\n\n")
                except Exception as e:
                    markdown_file.write(f"**Erro ao ler arquivo: {str(e)}**\n\n")

    print(f"Catálogo de arquivos gerado: {output_file}")


# Exemplo de uso
if __name__ == "__main__":
    directory_path = "/Users/thyagoluciano/Developer/projetos/idea-forge"
    ignore_dirs = [
        "venv",
        ".idea",
        ".git",
        "sample"
    ]
    ignore_files = [
        "*.pyc",  # Ignora todos os arquivos .pyc
        ".DS_Store",  # Ignora arquivos .DS_Store
        "*.log"  # Ignora todos os arquivos de log
        "code_2_md.py"
        ".gitignore"
    ]
    directory_to_markdown(directory_path, ignore_dirs, ignore_files)
```

## .env

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/.env`

```
# Reddit API
REDDIT_CLIENT_ID=YLAowFMWqNZ-3qs6COAYzA
REDDIT_CLIENT_SECRET=h0mdZvPnHqoIEj9XN9TyEHflp_0mbg
REDDIT_USER_AGENT=saas-ideas-db (by /u/thyagoluciano)

# Gemini API
GOOGLE_API_KEY=AIzaSyDcaPfYqUzZCVqCNKsKB87-sQNKArGJFJ4
GEMINI_MODEL=gemini-2.0-flash-exp

# Project Settings
SUBREDDIT_NAME = Entrepreneur
LIMIT_POSTS = 10
SORT_TYPE = hot
```

## app.log

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/app.log`

```log
2025-01-04 16:21:53,505 - INFO - Conexão com Reddit estabelecida com sucesso.
2025-01-04 16:21:53,505 - INFO - Conexão com Gemini estabelecida com sucesso.
2025-01-04 16:21:53,506 - INFO - Analisando o post: Thank you Thursday! - January 02, 2025 (1hrqg5q)
2025-01-04 16:21:53,506 - INFO - Upvotes: 4, Número de comentários: 10
2025-01-04 16:21:53,506 - INFO -   - Chelsea_M_Williams: I have a bunch of free resources for finances for ... (Upvotes: 4)
2025-01-04 16:21:53,506 - INFO -   - John_Gouldson: Love this idea. Here you go, a free link to one of... (Upvotes: 2)
2025-01-04 16:21:53,506 - INFO -   - Suly18: this is great! i run a digital marketing company h... (Upvotes: 2)
2025-01-04 16:21:53,506 - INFO -   - hanslee201: Hi! My name is Hans and I lead the partnership eff... (Upvotes: 2)
2025-01-04 16:21:53,506 - INFO -   - heythisischris: Hey ya"ll! Offering a free week Tabchat AI. Tabcha... (Upvotes: 2)
2025-01-04 16:21:53,506 - INFO -   - Feisty_Attorney_3811: Anyone looking to get into investing in stocks? I ... (Upvotes: 1)
2025-01-04 16:21:53,506 - INFO -   - Virtual_Welder_2467: Want to receive some insights about your project o... (Upvotes: 1)
2025-01-04 16:21:53,506 - INFO -   - Hopeful_Piglet2416: Happy New Year everyone! anyone who has a brillian... (Upvotes: 1)
2025-01-04 16:21:53,506 - INFO -   - johnrich85: Hey all. Im currently offering lifetime membership... (Upvotes: 1)
2025-01-04 16:22:03,492 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:22:04,452 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:22:07,945 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:22:08,082 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:22:10,902 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:22:10,903 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:22:10,904 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:22:10,904 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:24:28,945 - INFO - Conexão com Reddit estabelecida com sucesso.
2025-01-04 16:24:28,945 - INFO - Conexão com Gemini estabelecida com sucesso.
2025-01-04 16:24:36,592 - ERROR - Erro ao carregar o banco de dados: Expecting value: line 1 column 1 (char 0)
2025-01-04 16:24:36,593 - INFO - Analisando o post: Thank you Thursday! - January 02, 2025 (1hrqg5q)
2025-01-04 16:24:36,594 - INFO - Upvotes: 4, Número de comentários: 10
2025-01-04 16:24:36,594 - INFO -   - Chelsea_M_Williams: I have a bunch of free resources for finances for ... (Upvotes: 4)
2025-01-04 16:24:36,594 - INFO -   - John_Gouldson: Love this idea. Here you go, a free link to one of... (Upvotes: 2)
2025-01-04 16:24:36,594 - INFO -   - Suly18: this is great! i run a digital marketing company h... (Upvotes: 2)
2025-01-04 16:24:36,594 - INFO -   - hanslee201: Hi! My name is Hans and I lead the partnership eff... (Upvotes: 2)
2025-01-04 16:24:36,594 - INFO -   - heythisischris: Hey ya"ll! Offering a free week Tabchat AI. Tabcha... (Upvotes: 2)
2025-01-04 16:24:36,594 - INFO -   - Feisty_Attorney_3811: Anyone looking to get into investing in stocks? I ... (Upvotes: 1)
2025-01-04 16:24:36,594 - INFO -   - Virtual_Welder_2467: Want to receive some insights about your project o... (Upvotes: 1)
2025-01-04 16:24:36,594 - INFO -   - Hopeful_Piglet2416: Happy New Year everyone! anyone who has a brillian... (Upvotes: 1)
2025-01-04 16:24:36,594 - INFO -   - johnrich85: Hey all. Im currently offering lifetime membership... (Upvotes: 1)
2025-01-04 16:24:38,957 - INFO - Banco de dados salvo com sucesso.
2025-01-04 16:24:38,957 - INFO - Ideia 'None' adicionada ao banco de dados.
2025-01-04 16:24:38,957 - INFO - Ideia adicionada: Idea(reddit_content_id='1hrqg5q', product_name='None', problem='Businesses struggle to effectively reach their audience with important updates and content, facing low engagement on social media and email.', solution_description=None, implementation_score=None, market_viability_score=None, differentials='None', features='None')
2025-01-04 16:24:38,957 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:24:38,957 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:24:38,957 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:24:38,958 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:24:38,958 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:24:38,958 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:25:23,580 - INFO - Conexão com Reddit estabelecida com sucesso.
2025-01-04 16:25:23,580 - INFO - Conexão com Gemini estabelecida com sucesso.
2025-01-04 16:25:23,581 - ERROR - Erro ao carregar o banco de dados: Expecting value: line 1 column 1 (char 0)
2025-01-04 16:25:23,581 - INFO - Analisando o post: Thank you Thursday! - January 02, 2025 (1hrqg5q)
2025-01-04 16:25:23,581 - INFO - Upvotes: 4, Número de comentários: 10
2025-01-04 16:25:23,581 - INFO -   - Chelsea_M_Williams: I have a bunch of free resources for finances for ... (Upvotes: 4)
2025-01-04 16:25:23,581 - INFO -   - John_Gouldson: Love this idea. Here you go, a free link to one of... (Upvotes: 2)
2025-01-04 16:25:23,581 - INFO -   - Suly18: this is great! i run a digital marketing company h... (Upvotes: 2)
2025-01-04 16:25:23,581 - INFO -   - hanslee201: Hi! My name is Hans and I lead the partnership eff... (Upvotes: 2)
2025-01-04 16:25:23,581 - INFO -   - heythisischris: Hey ya"ll! Offering a free week Tabchat AI. Tabcha... (Upvotes: 2)
2025-01-04 16:25:23,581 - INFO -   - Feisty_Attorney_3811: Anyone looking to get into investing in stocks? I ... (Upvotes: 1)
2025-01-04 16:25:23,581 - INFO -   - Virtual_Welder_2467: Want to receive some insights about your project o... (Upvotes: 1)
2025-01-04 16:25:23,581 - INFO -   - Hopeful_Piglet2416: Happy New Year everyone! anyone who has a brillian... (Upvotes: 1)
2025-01-04 16:25:23,581 - INFO -   - johnrich85: Hey all. Im currently offering lifetime membership... (Upvotes: 1)
2025-01-04 16:26:41,571 - INFO - Conexão com Reddit estabelecida com sucesso.
2025-01-04 16:26:41,571 - INFO - Conexão com Gemini estabelecida com sucesso.
2025-01-04 16:26:41,571 - ERROR - Erro ao carregar o banco de dados: Expecting value: line 1 column 1 (char 0)
2025-01-04 16:26:41,571 - INFO - Analisando o post: Thank you Thursday! - January 02, 2025 (1hrqg5q)
2025-01-04 16:26:41,571 - INFO - Upvotes: 4, Número de comentários: 10
2025-01-04 16:26:41,571 - INFO -   - Chelsea_M_Williams: I have a bunch of free resources for finances for ... (Upvotes: 4)
2025-01-04 16:26:41,571 - INFO -   - John_Gouldson: Love this idea. Here you go, a free link to one of... (Upvotes: 2)
2025-01-04 16:26:41,571 - INFO -   - Suly18: this is great! i run a digital marketing company h... (Upvotes: 2)
2025-01-04 16:26:41,571 - INFO -   - hanslee201: Hi! My name is Hans and I lead the partnership eff... (Upvotes: 2)
2025-01-04 16:26:41,571 - INFO -   - heythisischris: Hey ya"ll! Offering a free week Tabchat AI. Tabcha... (Upvotes: 2)
2025-01-04 16:26:41,571 - INFO -   - Feisty_Attorney_3811: Anyone looking to get into investing in stocks? I ... (Upvotes: 1)
2025-01-04 16:26:41,571 - INFO -   - Virtual_Welder_2467: Want to receive some insights about your project o... (Upvotes: 1)
2025-01-04 16:26:41,571 - INFO -   - Hopeful_Piglet2416: Happy New Year everyone! anyone who has a brillian... (Upvotes: 1)
2025-01-04 16:26:41,571 - INFO -   - johnrich85: Hey all. Im currently offering lifetime membership... (Upvotes: 1)
2025-01-04 16:26:49,836 - INFO - Banco de dados salvo com sucesso.
2025-01-04 16:26:50,325 - INFO - Ideia 'None' adicionada ao banco de dados.
2025-01-04 16:26:52,515 - INFO - Ideia adicionada: Idea(reddit_content_id='1hrqg5q', product_name='None', problem='Businesses struggle to effectively reach their audience with important updates and content, facing low engagement on social media and email.', solution_description=None, implementation_score=3, market_viability_score=75, differentials='None', features='['Customizable push notifications', 'User segmentation', 'Real-time analytics', 'Scheduled notifications', 'Integration with other marketing tools']')
2025-01-04 16:26:56,161 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:26:56,749 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:27:03,292 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:27:03,293 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:27:03,293 - WARNING - A ideia com ID 1hrqg5q já existe no banco de dados.
2025-01-04 16:27:03,293 - WARNING - Não foi possível adicionar a ideia, pois ela já existe na base
2025-01-04 16:28:07,437 - INFO - Conexão com Reddit estabelecida com sucesso.
2025-01-04 16:28:07,438 - INFO - Conexão com Gemini estabelecida com sucesso.
2025-01-04 16:28:07,438 - INFO - Analisando o post: Thank you Thursday! - January 02, 2025 (1hrqg5q)
2025-01-04 16:28:07,438 - INFO - Upvotes: 4, Número de comentários: 10
2025-01-04 16:28:07,438 - INFO -   - Chelsea_M_Williams: I have a bunch of free resources for finances for ... (Upvotes: 4)
2025-01-04 16:28:07,438 - INFO -   - John_Gouldson: Love this idea. Here you go, a free link to one of... (Upvotes: 2)
2025-01-04 16:28:07,438 - INFO -   - Suly18: this is great! i run a digital marketing company h... (Upvotes: 2)
2025-01-04 16:28:07,438 - INFO -   - hanslee201: Hi! My name is Hans and I lead the partnership eff... (Upvotes: 2)
2025-01-04 16:28:07,438 - INFO -   - heythisischris: Hey ya"ll! Offering a free week Tabchat AI. Tabcha... (Upvotes: 2)
2025-01-04 16:28:07,438 - INFO -   - Feisty_Attorney_3811: Anyone looking to get into investing in stocks? I ... (Upvotes: 1)
2025-01-04 16:28:07,438 - INFO -   - Virtual_Welder_2467: Want to receive some insights about your project o... (Upvotes: 1)
2025-01-04 16:28:07,438 - INFO -   - Hopeful_Piglet2416: Happy New Year everyone! anyone who has a brillian... (Upvotes: 1)
2025-01-04 16:28:07,438 - INFO -   - johnrich85: Hey all. Im currently offering lifetime membership... (Upvotes: 1)
2025-01-04 16:28:07,440 - INFO - Banco de dados salvo com sucesso.
2025-01-04 16:28:07,440 - INFO - Ideia 'PushPro Engage' adicionada ao banco de dados.
2025-01-04 16:28:07,440 - INFO - Ideia adicionada: Idea(reddit_content_id='1hrqg5q', product_name='PushPro Engage', problem='Businesses struggle to effectively reach their audience with important updates and content, facing low engagement on social media and email.', solution_description=PushPro Engage is a SaaS platform that enables businesses to send push notifications directly to their audience"s phones, ensuring immediate attention and high engagement rates. It bypasses the limitations of social media algorithms and the low open rates of email newsletters. The platform offers customizable notifications, user segmentation and detailed analytics, providing a comprehensive solution for audience engagement., implementation_score=3, market_viability_score=75, differentials='['High engagement rates compared to email and social media', 'Guaranteed delivery', 'Ability to segment and target users effectively', 'Real-time analytics dashboard to track performance']', features='['Customizable push notifications', 'User segmentation', 'Real-time analytics', 'Scheduled notifications', 'Integration with other marketing tools']')
2025-01-04 16:28:07,440 - INFO - Banco de dados salvo com sucesso.
2025-01-04 16:28:07,441 - INFO - Ideia 'TabWise AI' adicionada ao banco de dados.
2025-01-04 16:28:07,441 - INFO - Ideia adicionada: Idea(reddit_content_id='1hrqg5q', product_name='TabWise AI', problem='Users often need to extract information or interact with the content of websites they are currently browsing, lacking a seamless way to do so.', solution_description=TabWise AI is a browser extension that lets users interact directly with any open web page using AI. It allows users to summarize, extract data, and engage in contextual conversations with the current webpage, simplifying workflows and boosting productivity.  The extension uses a large language model for advanced features, ensuring accurate and efficient results., implementation_score=4, market_viability_score=80, differentials='['Direct interaction with live webpages, not just pre-set knowledge', 'Ability to extract and export data from tables and unstructured content', 'Context awareness for better assistance and summaries', 'Integration with a cutting-edge large language model (LLM)']', features='['Chat with any tab', 'Data extraction (CSV/JSON)', 'Article summarization', 'Context-aware assistance', 'Integration with a large language model (LLM)']')
2025-01-04 16:28:07,441 - INFO - Banco de dados salvo com sucesso.
2025-01-04 16:28:07,441 - INFO - Ideia 'IdeaSpark' adicionada ao banco de dados.
2025-01-04 16:28:07,441 - INFO - Ideia adicionada: Idea(reddit_content_id='1hrqg5q', product_name='IdeaSpark', problem='Business owners are seeking new business opportunities that are not capital intensive.', solution_description=IdeaSpark is a SaaS platform for generating, validating, and refining business ideas that require low initial capital. The platform uses user-input data, market trends and AI to generate and validate ideas. It helps users discover opportunities in specific industries or niches, assess their feasibility and create basic business models. It aims to be a catalyst for entrepreneurial thinking by providing a structured approach to idea generation and validation., implementation_score=2, market_viability_score=60, differentials='['Focus on low-capital business models', 'User-driven insights and community feedback', 'Integration with market analysis tools for real-time data', 'AI-powered idea validation that goes beyond superficial analysis']', features='['AI-powered idea generation', 'Market validation tools', 'Low-capital business model templates', 'User-driven feedback system', 'Opportunity assessment reports']')
2025-01-04 16:28:07,442 - INFO - Banco de dados salvo com sucesso.
2025-01-04 16:28:07,442 - INFO - Ideia 'DirectoryEase' adicionada ao banco de dados.
2025-01-04 16:28:07,442 - INFO - Ideia adicionada: Idea(reddit_content_id='1hrqg5q', product_name='DirectoryEase', problem='Businesses and entrepreneurs need an easy way to build online directories without coding', solution_description=DirectoryEase is a no-code SaaS platform designed to enable anyone to create their online directory without needing to write a single line of code. It offers a wide variety of customizable templates, intuitive drag-and-drop editors and a suite of features to manage listings, users, and content. It"s ideal for small businesses, community groups, and entrepreneurs who want to launch a directory quickly and affordably., implementation_score=3, market_viability_score=85, differentials='['Intuitive no-code interface suitable for non-technical users', 'Highly customizable and feature-rich directory templates', 'Simplified user onboarding and directory management', 'Affordable pricing tiers for different needs', 'Integrations for monetization (payment gateways, advertisement)']', features='['Drag and drop directory builder', 'Customizable directory templates', 'User and listing management', 'Search and filter functionalities', 'Integration with payment gateways']')

```

## database/database.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/database/database.py`

```py
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
```

## database/__init__.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/database/__init__.py`

```py

```

## core/reddit_api.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/core/reddit_api.py`

```py
import praw
import time
from datetime import datetime
from config.config import Config
from utils.helpers import clean_text
from utils.logger import logger

class RedditAPI:
    def __init__(self):
        self.config = Config()
        try:
            self.reddit = praw.Reddit(
                client_id=self.config.REDDIT_CLIENT_ID,
                client_secret=self.config.REDDIT_CLIENT_SECRET,
                user_agent=self.config.REDDIT_USER_AGENT
            )
            logger.info("Conexão com Reddit estabelecida com sucesso.")
        except praw.exceptions.PRAWException as e:
            logger.error(f"Erro ao conectar com o Reddit: {e}")
            self.reddit = None

    def get_posts_and_comments(self, subreddit_name=None, limit=None, sort_by=None):
         """
         Obtém posts e seus comentários de um subreddit.

         Args:
             subreddit_name: Nome do subreddit a ser pesquisado.
             limit: Número máximo de posts a serem recuperados.
             sort_by: Tipo de ordenação ('hot', 'top', 'new', 'controversial').

         Returns:
             Uma lista de dicionários, onde cada dicionário representa um post e seus comentários.
         """
         if not subreddit_name:
            subreddit_name = self.config.SUBREDDIT_NAME
         if not limit:
           limit = int(self.config.LIMIT_POSTS)
         if not sort_by:
           sort_by = self.config.SORT_TYPE

         posts_data = []
         try:
             subreddit = self.reddit.subreddit(subreddit_name)

             if sort_by == 'hot':
                 posts = subreddit.hot(limit=limit)
             elif sort_by == 'top':
                 posts = subreddit.top(limit=limit)
             elif sort_by == 'new':
                 posts = subreddit.new(limit=limit)
             elif sort_by == 'controversial':
                 posts = subreddit.controversial(limit=limit)
             else:
                 raise ValueError("Invalid sort_by option")

             for post in posts:
                 post_data = {
                     "title": post.title,
                     "id": post.id,
                     "url": post.url,
                     "text": clean_text(post.selftext) if hasattr(post, 'selftext') else "",
                     "num_comments": post.num_comments,
                     "upvotes": post.ups,
                     "comments": []
                 }

                 post.comments.replace_more(limit=0)
                 for comment in post.comments.list():
                     post_data["comments"].append({
                         "author": comment.author.name if comment.author else "[deleted]",
                         "text": clean_text(comment.body),
                         "created": str(datetime.fromtimestamp(comment.created_utc)),
                         "upvotes": comment.ups
                     })
                 posts_data.append(post_data)
                 time.sleep(1)
         except praw.exceptions.PRAWException as e:
             logger.error(f"Erro ao obter posts do subreddit {subreddit_name}: {e}")
         return posts_data
```

## core/__init__.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/core/__init__.py`

```py

```

## core/gemini_api.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/core/gemini_api.py`

```py
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
```

## config/config.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/config/config.py`

```py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

    # Gemini API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", 'gemini-pro')  # Default gemini-pro

    # Project Settings
    SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME", "Entrepreneur")
    LIMIT_POSTS = os.getenv("LIMIT_POSTS", 10)
    SORT_TYPE = os.getenv("SORT_TYPE", 'hot')

```

## config/__init__.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/config/__init__.py`

```py

```

## utils/__init__.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/utils/__init__.py`

```py

```

## utils/logger.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/utils/logger.py`

```py
import logging

def setup_logger(name, log_file='app.log', level=logging.INFO):
    """Configura e retorna um logger."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

logger = setup_logger('saas_ideas')
```

## utils/helpers.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/utils/helpers.py`

```py
import re

def clean_text(text):
    """Remove quebras de linha, espaços extras e caracteres especiais do texto."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

## models/__init__.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/models/__init__.py`

```py

```

## models/idea.py

**Caminho completo**: `/Users/thyagoluciano/Developer/projetos/idea-forge/models/idea.py`

```py
class Idea:
    def __init__(
        self,
            reddit_content_id,
            product_name,
            problem,
            solution_description,
            implementation_score,
            market_viability_score,
            differentials,
            features
    ):
        self.reddit_content_id = reddit_content_id
        self.product_name = product_name
        self.problem = problem
        self.solution_description = solution_description
        self.implementation_score = implementation_score
        self.market_viability_score = market_viability_score
        self.differentials = differentials
        self.features = features

    def to_dict(self):
        return {
            "reddit_content_id": self.reddit_content_id,
            "product_name": self.product_name,
            "problem": self.problem,
            "solution_description": self.solution_description,
            "implementation_score": self.implementation_score,
            "market_viability_score": self.market_viability_score,
            "differentials": self.differentials,
            "features": self.features,
        }
    def __repr__(self):
      return f"Idea(reddit_content_id='{self.reddit_content_id}', product_name='{self.product_name}', problem='{self.problem}', solution_description={self.solution_description}, implementation_score={self.implementation_score}, market_viability_score={self.market_viability_score}, differentials='{self.differentials}', features='{self.features}')"
```

