from backend.ingestion.chunk_data import chunk_documents
from sentence_transformers import SentenceTransformer
import chromadb


def store_embeddings():
    print("🔄 Loading chunks...")
    chunks = chunk_documents()

    print("🔄 Loading local embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔄 Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="embeddings")

    collection = client.get_or_create_collection(name="campus_docs")

    print("🔄 Generating embeddings (LOCAL)...")

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()

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

    print(f"\n🎉 Stored {len(chunks)} embeddings successfully!")


if __name__ == "__main__":
    store_embeddings()