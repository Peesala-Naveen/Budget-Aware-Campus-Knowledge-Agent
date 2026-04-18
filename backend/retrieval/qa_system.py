import requests
import os
from dotenv import load_dotenv
from backend.retrieval.search import search_documents

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_answer(query):
    results = search_documents(query)

    context = ""
    for res in results:
        context += f"Source: {res['source']} Page: {res['page']}\n"
        context += res["text"] + "\n\n"

    prompt = f"""
You are a helpful campus assistant.

Answer ONLY from the context.
Give short answer + source.

Context:
{context}

Question:
{query}

Answer:
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    # Debug print (important)
    print("\nDEBUG RESPONSE:\n", data)

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"❌ API Error: {data}"


if __name__ == "__main__":
    query = input("Ask your question: ")
    answer = generate_answer(query)

    print("\n✅ Final Answer:\n")
    print(answer)