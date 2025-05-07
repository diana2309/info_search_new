from flask import Flask, request, render_template
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Загружаем документы и считаем TF-IDF
def load_documents(folder_path):
    documents = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                documents.append(f.read())
                filenames.append(filename)
    return documents, filenames


documents, filenames = load_documents("downloaded_pages")
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(documents)

# Поиск
def search(query, top_k=10):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, doc_vectors).flatten()
    ranked_indices = np.argsort(similarities)[::-1][:top_k]
    results = [(filenames[i], similarities[i]) for i in ranked_indices if similarities[i] > 0]
    return results

# Главная страница
@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form["query"]
        results = search(query)
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
