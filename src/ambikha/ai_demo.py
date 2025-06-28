"""
Example of using Ollama with ChromaDB for retrieval-augmented generation (RAG)
"""

import uuid
import currency_api
import chromadb
import requests
import re
from datetime import datetime


def setup_chromadb():
    """Initialize ChromaDB and create a collection"""
    # Initialize ChromaDB client
    chroma_client = chromadb.Client()

    # Create or get a collection
    try:
        collection = chroma_client.get_collection(name="example_docs")
        print("Using existing collection 'example_docs'")
    except:
        collection = chroma_client.create_collection(name="example_docs")
        print("Created new collection 'example_docs'")

    return collection


def update_exchange_rates(rates):
    rates = str(rates)
    rates = rates.strip("{").strip("}").replace(", ", "\n")
    rates = rates.split("\n")
    document_rates = ""
    for rate in rates:
        document_rates += f"The exchange rate for 1 USD to {rate[1:4]} is {rate[7:].strip()}\n"
    return document_rates


def load_chroma_data(collection):
    """Load sample data into ChromaDB collection"""
    # Sample documents for our knowledge base
    with open("beekeeping.txt", "r") as f:
        documents = f.read()
    documents += update_exchange_rates(currency_api.get_exchange_rate("EUR"))
    documents = [
        document
        for document in documents.split("\n")
        if len(document.strip()) > 0
    ]
    print(f"{len(documents)=}")

    # Create unique IDs for each document
    ids = [str(uuid.uuid4()) for _ in range(len(documents))]

    # Add documents to the collection
    collection.add(documents=documents, ids=ids)

    print(f"Added {len(documents)} documents to ChromaDB collection")
    return documents


def query_ollama(prompt, model="llama2"):
    """Query Ollama API and return a formatted response object"""
    url = "http://localhost:11434/api/generate"

    data = {"model": model, "prompt": prompt, "stream": False}

    # Call Ollama API
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = response.json()
        raw_text = response_data["response"]

        # Format the text for better readability
        formatted_text = raw_text.strip()

        # Add paragraph breaks for readability
        formatted_text = re.sub(r"\n{2,}", "\n\n", formatted_text)

        # If response contains markdown-style lists, format them better
        if re.search(r"^\d+\.", formatted_text, re.MULTILINE):
            list_items = re.findall(
                r"^\d+\.\s*(.*?)$", formatted_text, re.MULTILINE
            )
            if list_items:
                formatted_text = formatted_text.replace(
                    "\n".join(
                        [
                            f"{i + 1}. {item}"
                            for i, item in enumerate(list_items)
                        ]
                    ),
                    "\n• " + "\n• ".join(list_items),
                )

        return {
            "raw_response": raw_text,
            "formatted_response": formatted_text,
            "model": response_data.get("model", model),
            "created_at": response_data.get(
                "created_at", datetime.now().isoformat()
            ),
            "processing_time": f"{response_data.get('total_duration', 0) / 1000000:.2f}ms",
            "tokens_generated": response_data.get("eval_count", 0),
        }
    else:
        return {"error": f"Error: {response.status_code} - {response.text}"}


def rag_with_ollama(query, collection):
    """
    Perform retrieval-augmented generation with Ollama and ChromaDB
    """
    num_results = 5
    # 1. Query ChromaDB to find relevant documents
    results = collection.query(query_texts=[query], n_results=num_results)

    # Extract the retrieved documents
    retrieved_docs = results["documents"][0]

    # 2. Create a prompt with context for Ollama
    context = "\n".join(retrieved_docs)

    prompt = f"""
    You are a helpful assistant that answers questions based on the following context:
    
    Context:
    {context}
    
    Question: {query}
    Please provide a detailed answer based only on the information in the context.
    If the context doesn't contain relevant information, say so.
    
    """

    # 3. Generate response using Ollama
    response = query_ollama(prompt)

    return {
        "query": query,
        "retrieved_context": retrieved_docs,
        "ollama_response": response,
    }


def submit_ai_query(query, collection):
    """Main function to demonstrate the RAG workflow"""

    try:
        result = rag_with_ollama(query, collection)
        print(result)

        print("\nRETRIEVED CONTEXT:")
        for i, doc in enumerate(result["retrieved_context"]):
            print(f"{i + 1}. {doc}")

        print("\nOLLAMA RESPONSE:")
        print(result["ollama_response"])
    except Exception as e:
        print(f"Error processing query: {str(e)}")

    print("\nAdditional notes:")
    print("1. Make sure Ollama is running locally (http://localhost:11434)")
    print(
        "2. You may need to download a model with 'ollama pull llama2' if not already done"
    )
    print(
        "3. For production use, consider using proper embeddings instead of ChromaDB's default"
    )
    return result["ollama_response"]["formatted_response"]
