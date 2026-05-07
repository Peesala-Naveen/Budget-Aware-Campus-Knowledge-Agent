from backend.ingestion.chunk_data import chunk_documents
from backend.retrieval.search import get_embedding
import chromadb


def store_embeddings():
    print("🔄 Loading chunks...")
    chunks = chunk_documents()

    print("🔄 Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="embeddings")

    collection = client.get_or_create_collection(name="campus_docs")

    print("🔄 Generating embeddings using HuggingFace API...")

    for i, chunk in enumerate(chunks):
        try:
            # 🔥 Get embedding from HuggingFace
            embedding = get_embedding(chunk["text"])[0]

            collection.add(
                ids=[str(i)],
                embeddings=[embedding],
                documents=[chunk["text"]],
                metadatas=[{
                    "source": chunk["source"],
                    "page": chunk["page"]
                }]
            )

            print(f"✅ Stored chunk {i+1}/{len(chunks)}")

        except Exception as e:
            print(f"❌ Error at chunk {i}: {e}")

    print(f"\n🎉 Stored {len(chunks)} embeddings successfully!")


# 🚨 ENTRY POINT
if __name__ == "__main__":
    store_embeddings()