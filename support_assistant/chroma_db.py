import chromadb

from support_assistant.embeddings import (
    load_documents,
    generate_embeddings
)

client = chromadb.PersistentClient(
    path="support_assistant/chroma_db"
)

COLLECTION_NAME = "zepto_support"

try:
    client.delete_collection(COLLECTION_NAME)
except Exception:
    pass

collection = client.create_collection(
    name=COLLECTION_NAME
)


def main():

    print("Loading Documents...")

    ids, documents = load_documents()

    print("Generating Embeddings...")

    embeddings = generate_embeddings(documents)

    print("Saving to ChromaDB...")

    collection.add(

        ids=ids,

        documents=documents,

        embeddings=embeddings.tolist()

    )

    print()

    print("Collection :", collection.name)

    print("Documents Stored :", collection.count())


if __name__ == "__main__":
    main()