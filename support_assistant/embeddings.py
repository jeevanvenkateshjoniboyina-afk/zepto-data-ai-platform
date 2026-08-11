import os

from sentence_transformers import SentenceTransformer
DOCS_FOLDER = "support_assistant/docs"
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)
def load_documents():

    documents = []

    ids = []

    for filename in sorted(os.listdir(DOCS_FOLDER)):

        if filename.endswith(".txt"):

            file_path = os.path.join(DOCS_FOLDER, filename)

            with open(file_path, "r", encoding="utf-8") as file:

                text = file.read()

            documents.append(text)

            ids.append(filename.replace(".txt", ""))

    return ids, documents
def generate_embeddings(documents):

    embeddings = model.encode(documents)

    return embeddings
def main():

    ids, documents = load_documents()

    embeddings = generate_embeddings(documents)

    print("Documents Loaded :", len(documents))

    print("Embeddings Generated :", len(embeddings))

    print()

    print("Embedding Dimension :", len(embeddings[0]))
if __name__ == "__main__":
    main()