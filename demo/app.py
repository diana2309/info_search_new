from flask import Flask, request, render_template
import os
import math
from collections import Counter

app = Flask(__name__)

def load_documents(folder_path):
    documents = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(text)
                filenames.append(filename)
    return documents, filenames

def preprocess(text):
    tokens = text.lower().split()
    tokens = [token.strip(".,!?;:()[]\"") for token in tokens]
    return tokens

def compute_tf(doc_tokens):
    tf = {}
    total_terms = len(doc_tokens)
    term_counts = Counter(doc_tokens)
    for term, count in term_counts.items():
        tf[term] = count / total_terms
    return tf

def compute_idf(all_docs_tokens):
    import collections

    N = len(all_docs_tokens)
    document_frequency = collections.defaultdict(int)

    for doc in all_docs_tokens:
        unique_terms = set(doc)
        for term in unique_terms:
            document_frequency[term] += 1

    idf = {term: math.log(N / (1 + df)) for term, df in document_frequency.items()}
    return idf


def compute_tfidf(tf, idf):
    return {term: tf_val * idf[term] for term, tf_val in tf.items() if term in idf}

def cosine_similarity(vec1, vec2):
    dot = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in set(vec1) | set(vec2))
    norm1 = math.sqrt(sum(v**2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v**2 for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

# Загружаем и векторизуем документы
documents, filenames = load_documents("downloaded_pages")
documents_tokens = [preprocess(doc) for doc in documents]
tfs = [compute_tf(tokens) for tokens in documents_tokens]
idf = compute_idf(documents_tokens)
tfidfs = [compute_tfidf(tf, idf) for tf in tfs]


def search(query, top_k=10):
    query_tokens = preprocess(query)
    query_tf = compute_tf(query_tokens)
    query_vec = compute_tfidf(query_tf, idf)

    sims = [cosine_similarity(query_vec, doc_vec) for doc_vec in tfidfs]
    ranked = sorted(zip(filenames, sims), key=lambda x: x[1], reverse=True)
    return [(fn, score) for fn, score in ranked if score > 0][:top_k]

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
