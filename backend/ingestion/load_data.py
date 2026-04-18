import os
from pypdf import PdfReader

DATA_PATH = "data"

# ❌ PDFs to ignore (image-based or not useful)
IGNORE_FILES = ["Infastructure.pdf"]


def load_pdfs():
    documents = []

    for file in os.listdir(DATA_PATH):

        # Skip unwanted files
        if file in IGNORE_FILES:
            print(f"Skipping {file} (image-based)")
            continue

        if file.endswith(".pdf"):
            file_path = os.path.join(DATA_PATH, file)
            reader = PdfReader(file_path)

            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()

                # Skip empty pages
                if text and text.strip():
                    documents.append({
                        "text": text,
                        "source": file,
                        "page": page_num + 1
                    })

    return documents


if __name__ == "__main__":
    docs = load_pdfs()

    print(f"\n✅ Loaded {len(docs)} valid pages\n")

    # Show sample
    for i in range(min(2, len(docs))):
        print("-----")
        print("Source:", docs[i]["source"])
        print("Page:", docs[i]["page"])
        print("Text:", docs[i]["text"][:200])