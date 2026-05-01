import chromadb
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


# 🔥 HuggingFace Embedding Function
def get_embedding(text):
    response = requests.post(
        "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
        headers={
            "Authorization": f"Bearer {HF_TOKEN}"
        },
        json={"inputs": text}
    )

    if response.status_code != 200:
        print("ERROR:", response.text)
        return None

    result = response.json()
    return result[0]

def search_documents(query, top_k=3):
    print("🔄 Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="embeddings")

    collection = client.get_collection(name="campus_docs")

    print("🔄 Encoding query using HuggingFace API...")
    query_embedding = get_embedding(query)

    if query_embedding is None:
        raise Exception("❌ HuggingFace embedding failed")

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