# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de dependências e instale as bibliotecas necessárias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o container
COPY . .

# Exponha a porta utilizada pela aplicação (ajuste se necessário)
EXPOSE 80

# Defina o comando de inicialização da aplicação
CMD ["python", "app.py"]
