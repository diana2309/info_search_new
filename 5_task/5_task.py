import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


def load_documents(folder_path):
    documents = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                documents.append(f.read())
                filenames.append(filename)
    return documents, filenames


def load_tfidf_data(tfidf_folder):
    tfidf_data = {}
    for filename in os.listdir(tfidf_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(tfidf_folder, filename), "r", encoding="utf-8") as f:
                terms = []
                tfidf_values = []
                for line in f:
                    term, _, tfidf = line.strip().split()
                    terms.append(term)
                    tfidf_values.append(float(tfidf))
                tfidf_data[filename] = dict(zip(terms, tfidf_values))
    return tfidf_data


# Векторизация документов и запроса
def vectorize_documents(documents):
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documents)
    return vectorizer, doc_vectors


# Поиск по запросу
def search(query, vectorizer, doc_vectors, filenames, top_k=10):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, doc_vectors).flatten()
    ranked_indices = np.argsort(similarities)[::-1][:top_k]
    results = [(filenames[i], similarities[i]) for i in ranked_indices]
    return results


if __name__ == "__main__":
    documents, filenames = load_documents("downloaded_pages")
    vectorizer, doc_vectors = vectorize_documents(documents)

    query = "фестиваль"
    results = search(query, vectorizer, doc_vectors, filenames)

    for filename, score in results:
        print(f"{filename}: {score:.4f}")