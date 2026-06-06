from langchain_huggingface import HuggingFaceEmbeddings

def main():
    print("Loading FREE embedding model...")

    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Word embeddings
    vec1 = embedding.embed_query("apple")
    vec2 = embedding.embed_query("iphone")

    print("\nVector for 'apple':", vec1[:10], "...")
    print("Vector length:", len(vec1))

    # Simple cosine similarity (manual, reliable)
    from sklearn.metrics.pairwise import cosine_similarity

    similarity = cosine_similarity([vec1], [vec2])[0][0]

    print("\nSimilarity between apple and iphone:", similarity)


if __name__ == "__main__":
    main()