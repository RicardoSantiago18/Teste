from app.rag_chain import create_chain
from langchain_core.prompts import PromptTemplate

def gerar_relatorio_final(llm, history, maintenance_mode):
    """Gera um relatório técnico formatado com base no histórico da conversa."""
    print("\n⏳ Gerando relatório técnico...")
    
    prompt_relatorio = PromptTemplate.from_template(
        """
        Atue como um Engenheiro Sênior. Com base no histórico de conversa abaixo, gere um RELATÓRIO TÉCNICO DE MANUTENÇÃO formal.
        
        TIPO DE MANUTENÇÃO: {mode}
        
        HISTÓRICO DA INTERVENÇÃO:
        {history}
        
        O relatório deve conter:
        1. Resumo do Problema/Solicitação
        2. Diagnóstico ou Procedimentos Realizados (Baseado na conversa)
        3. Solução Sugerida ou Ações Tomadas
        4. Recomendações Futuras
        
        Gere apenas o texto do relatório.
        """
    )
    
    chain_relatorio = prompt_relatorio | llm
    formatted_history = "\n".join([f"Técnico: {h[0]}\nIA: {h[1]}" for h in history])
    
    relatorio = chain_relatorio.invoke({"mode": maintenance_mode, "history": formatted_history})
    return relatorio

def main():
    # Carrega a chain, a busca web e o llm puro (para o relatório)
    rag_chain, web_search, llm = create_chain()

    print("🔧 IA DE MANUTENÇÃO INDUSTRIAL INICIADA 🔧")
    print("---------------------------------------------")

    # 1. Definição do Tipo de Manutenção
    while True:
        tipo = input("\nQual o tipo de manutenção? (1-Corretiva / 2-Preventiva): ").strip()
        if tipo == "1" or "corretiva" in tipo.lower():
            maintenance_mode = "Manutenção Corretiva (Foco em reparo e diagnóstico)"
            print(f"✅ Modo selecionado: {maintenance_mode}")
            break
        elif tipo == "2" or "preventiva" in tipo.lower():
            maintenance_mode = "Manutenção Preventiva (Foco em checklist e inspeção)"
            print(f"✅ Modo selecionado: {maintenance_mode}")
            break
        else:
            print("❌ Opção inválida. Digite 1 ou 2.")

    history = [] # Lista para guardar [(pergunta, resposta)]
    print("\nDigite sua dúvida ou descreva o problema (Digite 'relatorio' para encerrar e gerar o documento).")

    # 2. Loop de Conversa
    while True:
        query = input("\n👤 Técnico: ")

        if query.lower() in ["sair", "exit"]:
            print("Encerrando sem gerar relatório.")
            break
        
        if query.lower() in ["relatorio", "gerar relatorio", "fim"]:
            relatorio = gerar_relatorio_final(llm, history, maintenance_mode)
            print("\n" + "="*60)
            print("📄 RELATÓRIO DE MANUTENÇÃO GERADO")
            print("="*60)
            print(relatorio)
            
            # Opcional: Salvar em arquivo
            with open("relatorio_manutencao.txt", "w", encoding="utf-8") as f:
                f.write(relatorio)
            print("\n💾 Relatório salvo em 'relatorio_manutencao.txt'")
            break

        # Formata o histórico como string para o prompt
        history_str = "\n".join([f"User: {h[0]}\nAI: {h[1]}" for h in history[-3:]]) # Mantém as últimas 3 trocas para contexto imediato

        # Invoca a chain passando todas as variáveis
        input_data = {
            "question": query, 
            "maintenance_mode": maintenance_mode,
            "history": history_str
        }
        
        # Como usamos RunnablePassthrough no chain, precisamos passar um dicionário compatível
        # Mas o 'rag_chain' original espera apenas a string se não configurarmos o .invoke corretamente com dict
        # Ajuste técnico: O RunnablePassthrough pega o input direto. 
        # Vamos invocar passando o dicionário, pois ajustamos o prompt para esperar chaves.
        
        answer = rag_chain.invoke(input_data)

        print(f"\n🤖 IA ({maintenance_mode}):")
        print(answer)
        
        # Salva no histórico
        history.append((query, answer))

        # Busca Web (Opcional - somente se a resposta do RAG sugerir ou se o usuário pedir)
        # Para simplificar, mantivemos automático, mas você pode colocar uma condição
        print("\n🌐 Fontes Complementares (Web):")
        try:
            web_results = web_search.invoke(query)
            for item in web_results:
                print(f"- {item['content'][:150]}...") # Limita o tamanho do texto web
        except Exception as e:
            print("Não foi possível buscar na web no momento.")

        print("-" * 50)

if __name__ == "__main__":
    main()