from backend.ingestion.load_data import load_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents():
    docs = load_pdfs()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # size of each chunk
        chunk_overlap=50     # overlap for context
    )

    chunks = []

    for doc in docs:
        split_texts = text_splitter.split_text(doc["text"])

        for chunk in split_texts:
            chunks.append({
                "text": chunk,
                "source": doc["source"],
                "page": doc["page"]
            })

    return chunks


if __name__ == "__main__":
    chunks = chunk_documents()

    print(f"\n✅ Created {len(chunks)} chunks\n")

    # Show sample
    for i in range(min(2, len(chunks))):
        print("-----")
        print("Source:", chunks[i]["source"])
        print("Page:", chunks[i]["page"])
        print("Chunk:", chunks[i]["text"][:200])