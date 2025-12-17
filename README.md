✅ Passo a passo para rodar
1️⃣ Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate   # Windows
# ou
source venv/bin/activate  # Linux

2️⃣ Instalar dependências
pip install -U \
langchain-core \
langchain-community \
langchain-huggingface \
langchain-text-splitters \
faiss-cpu \
sentence-transformers \
pypdf \
python-dotenv \
tavily-python

3️⃣ Instalar e rodar o LLM local (Ollama)

Instalar: https://ollama.com

Baixar o modelo:

ollama pull mistral:7b-instruct

Subir o servidor:

ollama serve

4️⃣ Adicionar os manuais técnicos

Coloque os PDFs em:

data/pdfs/

⚠️ Os PDFs precisam conter texto selecionável (PDF escaneado precisa de OCR).

5️⃣ Indexar os PDFs (RAG)
python app/ingest.py

Isso cria o banco vetorial em:

data/vectorstore/

6️⃣ Configurar busca web (Tavily)

Criar o arquivo .env na raiz:

TAVILY_API_KEY=sua_chave_aqui

7️⃣ Rodar a IA

Sempre a partir da raiz do projeto:

python -m app.main
