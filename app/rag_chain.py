from dotenv import load_dotenv
from operator import itemgetter  # <--- Importação necessária para corrigir o erro

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser

from app.llm import load_llm

VECTOR_DIR = "data/vectorstore"

load_dotenv()

def create_chain():
    llm = load_llm()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        VECTOR_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template(
        """
        Você é um assistente especialista em manutenção industrial.
        
        MODO DE OPERAÇÃO: {maintenance_mode}
        
        Se o modo for "Corretiva": Foque em diagnosticar a falha, identificar a causa raiz e sugerir reparos imediatos.
        Se o modo for "Preventiva": Foque em checklists, inspeção de desgaste e procedimentos de rotina.

        HISTÓRICO DA CONVERSA:
        {history}

        CONTEXTO DOS MANUAIS (Técnico):
        {context}

        PERGUNTA ATUAL DO USUÁRIO:
        {question}

        Responda de forma técnica, guiando o técnico passo-a-passo.
        Resposta:
        """
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # --- CORREÇÃO AQUI ---
    # Usamos itemgetter para pegar apenas os campos específicos do dicionário de entrada
    rag_chain = (
        {
            "context": itemgetter("question") | retriever | format_docs,
            "question": itemgetter("question"),
            "maintenance_mode": itemgetter("maintenance_mode"),
            "history": itemgetter("history")
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    web_search = TavilySearchResults(k=3)

    return rag_chain, web_search, llm