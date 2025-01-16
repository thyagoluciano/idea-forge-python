# Use uma imagem base do Python 3.11.
FROM python:3.11.5-slim-bookworm AS builder

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho.
COPY requirements.txt ./

# Instala as dependências usando o pip.
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto para o diretório de trabalho.
COPY . .

# Define a imagem de produção com o mínimo de dependências.
FROM python:3.11.5-slim-bookworm

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Copia os arquivos de instalação e dependências do builder stage
COPY --from=builder /app/requirements.txt ./
COPY --from=builder /app/src ./src

# Instala as dependências apenas em runtime
RUN pip install --no-cache-dir -r requirements.txt

# Adiciona o diretorio src ao PYTHONPATH
ENV PYTHONPATH=/app/src

# Lista o conteúdo do diretório /app/src
RUN ls -la /app/src

EXPOSE 8081

# Define o comando para executar a aplicação.
CMD ["python", "src/main.py"]