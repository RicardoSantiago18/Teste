from app.rag_chain import create_chain

def main():
    rag_chain, web_search = create_chain()

    print("IA de Manutenção iniciada. Digite 'sair' para encerrar.\n")

    while True:
        query = input("Pergunta: ")

        if query.lower() == "sair":
            break

        answer = rag_chain.invoke(query)

        print("\nResposta (Manuais):")
        print(answer)

        print("\nComplemento (Web):")
        web_results = web_search.invoke(query)
        for item in web_results:
            print("-", item["content"])

        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    main()
