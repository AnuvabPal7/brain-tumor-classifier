import argparse
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

CHROMA_PATH = "chroma"


def get_relevant_context(db, query):
    """Retrieve best matching documents"""
    results = db.similarity_search_with_relevance_scores(query, k=5)

    if not results:
        return None, None

    score = results[0][1]
    if score < 0.40:
        return None, score

    context = "\n\n---\n\n".join(
        [doc.page_content[:1000] for doc, _ in results]
    )

    return context, score


def build_prompt(context, query):
    return f"""
You are an intelligent document-based AI assistant.

Your task is to answer ONLY using the provided context.

RULES:
- Do NOT use outside knowledge
- Do NOT guess information
- If answer is missing, say: "Not enough information in the document."
- Be clear, structured, and concise

Context:
{context}

Question:
{query}

Answer:
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str)
    args = parser.parse_args()

    query = args.query_text

    print("\n🚀 RAG System Starting...")

    # Embeddings
    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Load DB
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding
    )

    print("📂 Vector database loaded")

    # Retrieve context
    context, score = get_relevant_context(db, query)

    if context is None:
        print("\n⚠️ No strong relevant information found in documents.")
        return

    print(f"🔎 Relevance Score: {score:.2f}")

    # Build prompt
    prompt = build_prompt(context, query)

    print("\n🤖 Sending to local LLM (Ollama)...")

    # LLM (lightweight for laptop)
    llm = OllamaLLM(
        model="phi3",
        temperature=0
    )

    answer = llm.invoke(prompt)

    print("\n================ FINAL ANSWER ================\n")
    print(answer)
    print("\n=============================================\n")


if __name__ == "__main__":
    main()