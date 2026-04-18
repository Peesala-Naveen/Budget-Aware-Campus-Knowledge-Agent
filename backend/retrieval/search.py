import chromadb
from sentence_transformers import SentenceTransformer


def search_documents(query, top_k=3):
    print("🔄 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔄 Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="embeddings")

    collection = client.get_collection(name="campus_docs")

    print("🔄 Encoding query...")
    query_embedding = model.encode(query).tolist()

    print("🔍 Searching...")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    final_results = []

    for doc, meta in zip(documents, metadatas):
        final_results.append({
            "text": doc,
            "source": meta["source"],
            "page": meta["page"]
        })

    return final_results


if __name__ == "__main__":
    query = input("Enter your question: ")

    results = search_documents(query)

    print("\n✅ Top Results:\n")

    for i, res in enumerate(results):
        print(f"Result {i+1}")
        print("Source:", res["source"])
        print("Page:", res["page"])
        print("Text:", res["text"][:200])
        print("-----")