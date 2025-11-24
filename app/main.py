from .graph import run_agent

def main():
    print("Soc Rag Assistant")
    print("Ask Hardware/SoC questions. Type 'exit' to quit. \n")

    while True:
        question = input("You: ").strip()

        if not question:
            continue
        if question.lower() in {"exit", "quit", "bye","by"}:
            print("See ya, Bye!")
            break

        result = run_agent(question)

        print("\nAssistant:")
        print(result.get("answer", ""))

        mode = result.get("mode", "unknown")
        print(f"\n [Mode used: {mode}]")

        sources = result.get("sources") or []
        if sources:
            print("Sources (from RAG):")
            for src in sources:
                print(f" - {src['source']} (page {src['source']})")

            print("\n" + "-" * 60 + "\n")
        else:
            print("Sources: (No RAG context used)")

            print("\n" + "-" * 60 + "\n")

if __name__ =="__main__":
    main()