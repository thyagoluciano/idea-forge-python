import re

def clean_text(text):
    """Remove quebras de linha, espaços extras e caracteres especiais do texto."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text