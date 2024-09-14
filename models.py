from db import documents_collection


def serialize_document(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def rag_search(query, top_k=5):

    results = list(
        documents_collection.find({"$text": {"$search": query}}).limit(top_k)
    )
    results = [serialize_document(doc) for doc in results]

    if not results:
        return {"answer": "No relevant documents found."}

    context = " ".join([doc["content"] for doc in results])

    return {"documents": results}
