import os


def get_language_from_extension(file_extension):
    """
    Retorna a linguagem correspondente à extensão do arquivo.

    :param file_extension: Extensão do arquivo (sem o ponto)
    :return: String representando a linguagem para o bloco de código Markdown
    """
    language_map = {
        'py': 'python',
        'js': 'javascript',
        'html': 'html',
        'css': 'css',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'go': 'go',
        'rs': 'rust',
        'rb': 'ruby',
        'php': 'php',
        'ts': 'typescript',
        'sh': 'bash',
        'sql': 'sql',
        'md': 'markdown',
        'json': 'json',
        'xml': 'xml',
        'yaml': 'yaml',
        'yml': 'yaml',
        'txt': 'text'
    }
    return language_map.get(file_extension.lower(), '')


def scan_directory(directory, output_file, ignore_dirs=None, ignore_files=None):
    """
    Escaneia um diretório e salva a estrutura em um arquivo Markdown.

    :param directory: Caminho do diretório a ser escaneado
    :param output_file: Nome do arquivo de saída Markdown
    :param ignore_dirs: Lista de diretórios a serem ignorados
    :param ignore_files: Lista de arquivos a serem ignorados
    """
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []

    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(directory):
            # Ignora diretórios especificados
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                # Ignora arquivos especificados
                if file in ignore_files:
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)

                # Obtém a extensão do arquivo e a linguagem correspondente
                _, file_extension = os.path.splitext(file)
                language = get_language_from_extension(file_extension[1:])  # Remove o ponto da extensão

                # Escreve o cabeçalho com o caminho do arquivo
                f.write(f"## {relative_path}\n")
                f.write(f"```{language}\n")

                # Lê e escreve o conteúdo do arquivo
                try:
                    with open(file_path, 'r', encoding='utf-8') as source_file:
                        content = source_file.read()
                        f.write(content)
                except Exception as e:
                    f.write(f"Erro ao ler o arquivo: {str(e)}")

                f.write("\n```\n\n")


def main(directory, output_file, ignore_dirs=None, ignore_files=None):
    """
    Função principal que inicia o processo de escaneamento.

    :param directory: Caminho do diretório a ser escaneado
    :param output_file: Nome do arquivo de saída Markdown
    :param ignore_dirs: Lista de diretórios a serem ignorados (opcional)
    :param ignore_files: Lista de arquivos a serem ignorados (opcional)
    """
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []

    scan_directory(directory, output_file, ignore_dirs, ignore_files)
    print(f"Arquivo Markdown '{output_file}' criado com sucesso!")


if __name__ == "__main__":
    main(
        directory="/Users/thyagoluciano/Developer/projetos/bemysaas/idea-forge/idea-forge-python",
        # directory="/Users/thyagoluciano/Developer/projetos/bemysaas/saas-scaffold",
        output_file="catalogo_arquivos.md",
        ignore_dirs=[".git", "venv", "old_src", ".idea", ".git", ".next", "node_modules", "_files"],
        ignore_files=["README.md", ".gitignore", "catalogo_arquivos.md", "code_2_md.py", ".env", "app.log", "pnpm-lock.yaml", "package-lock.json", "package.json", "_files/node_modules__pnpm_0819a1._.js"]
    )
