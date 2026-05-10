import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("reports")


def store_document(doc_id, content):
    collection.add(
        documents=[content],
        ids=[doc_id]
    )


def search_document(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    return results