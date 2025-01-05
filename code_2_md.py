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