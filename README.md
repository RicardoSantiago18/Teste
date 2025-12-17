# 🤖 IA de Manutenção Industrial (LLM Local)

Este projeto implementa uma **IA de teste para apoio à manutenção industrial**, executada **localmente**, utilizando um **LLM open‑source**, **manuais técnicos em PDF** (RAG) e **busca na web via Tavily** para complementar as respostas.

O objetivo é servir como **prova de conceito** para avaliar o uso de LLMs na análise de falhas, manutenção preventiva/corretiva e apoio técnico a engenheiros.

---

## 🧠 Visão Geral

A IA é capaz de:

* 📄 Ler e indexar **manuais técnicos em PDF**
* 🔍 Recuperar informações relevantes via **RAG (Retrieval‑Augmented Generation)**
* 🌐 Complementar respostas com **busca na web (Tavily Search)**
* 🤖 Executar um **LLM local (Mistral 7B Instruct via Ollama)**
* 🖥️ Rodar localmente (offline, exceto web search)

---

## 🏗️ Arquitetura

```
Usuário
  ↓
Pergunta
  ↓
RAG (FAISS + PDFs)
  ↓
LLM Local (Mistral 7B)
  ↓
Resposta técnica
  +
Complemento via Tavily (Web)
```

---

## 📁 Estrutura do Projeto

```
project-root/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # Interface CLI
│   ├── rag_chain.py     # RAG (LCEL)
│   ├── llm.py           # Conexão com LLM local
│   └── ingest.py        # Ingestão e indexação dos PDFs
│
├── data/
│   ├── pdfs/            # Manuais técnicos
│   └── vectorstore/     # Índice FAISS
│
├── .env                 # Chave da Tavily
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos

* Python **3.10+**
* Ollama (LLM local)
* CPU ou GPU (quantização permite uso em máquinas modestas)

---

## 🚀 Instalação

### 1️⃣ Criar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# ou
source venv/bin/activate # Linux
```

---

### 2️⃣ Instalar dependências

```bash
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
```

---

### 3️⃣ Instalar e rodar o LLM local (Ollama)

1. Instale o Ollama: [https://ollama.com](https://ollama.com)
2. Baixe o modelo:

```bash
ollama pull mistral:7b-instruct
```

3. Inicie o servidor:

```bash
ollama serve
```

---

## 📄 Ingestão de PDFs (RAG)

1. Coloque os manuais técnicos em:

```
data/pdfs/
```

⚠️ Os PDFs devem conter **texto selecionável** (PDFs escaneados exigem OCR).

2. Execute a indexação:

```bash
python app/ingest.py
```

Isso criará o índice vetorial em `data/vectorstore/`.

---

## 🌐 Configuração da Busca Web (Tavily)

Crie um arquivo `.env` na raiz do projeto:

```env
TAVILY_API_KEY=SUA_CHAVE_AQUI
```

A chave pode ser obtida em: [https://tavily.com](https://tavily.com)

---

## ▶️ Executar a IA

Sempre execute a partir da **raiz do projeto**:

```bash
python -m app.main
```

---

## 🧪 Exemplo de Uso

```
Pergunta:
Quais são as causas de vibração excessiva em uma máquina industrial?
```

A resposta será:

* 📄 Baseada nos **manuais técnicos**
* 🔎 Complementada com **informações recentes da web**

---

## 🧩 Tecnologias Utilizadas

* **Python**
* **LangChain (LCEL)**
* **FAISS** (vetorização local)
* **Sentence‑Transformers** (embeddings)
* **Ollama** (LLM local)
* **Mistral 7B Instruct** (open‑source)
* **Tavily Search** (busca web)

---

## 🔮 Próximos Passos (Evolução)

* [ ] Unificar resposta de PDFs + Web em um único output
* [ ] Criar prompt system profissional (engenharia de manutenção)
* [ ] Geração automática de relatório de manutenção
* [ ] API REST com FastAPI
* [ ] Interface web
* [ ] Suporte a OCR para PDFs escaneados

---

## 📜 Licença

Projeto de teste / prova de conceito para fins educacionais e experimentais.
