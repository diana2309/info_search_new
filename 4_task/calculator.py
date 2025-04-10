import os
import math
from collections import defaultdict, Counter

LEMMA_DIR = '../../lemmas'
TOKEN_DIR = '../../downloaded_pages'
OUT_TOKENS_DIR = '../../tfidf_tokens'
OUT_LEMMAS_DIR = '../../tfidf_lemmas'

os.makedirs(OUT_TOKENS_DIR, exist_ok=True)
os.makedirs(OUT_LEMMAS_DIR, exist_ok=True)

def compute_idf(doc_term_counts, total_docs):
    df = defaultdict(int)
    for doc in doc_term_counts:
        for term in set(doc_term_counts[doc]):
            df[term] += 1

    idf = {term: math.log(total_docs / df[term]) for term in df}
    return idf

def process_documents(folder_path, is_lemma=False):
    doc_term_counts = {}
    total_terms_per_doc = {}

    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue

        doc_id = int(''.join(filter(str.isdigit, filename)))
        path = os.path.join(folder_path, filename)
        term_list = []

        with open(path, 'r', encoding='utf-8') as f:
            if is_lemma:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        term_list.append(parts[0])  # берем только лемму
            else:
                content = f.read()
                words = content.split()
                words = [w for w in words if w.isalpha()]  # убираем мусор
                term_list = [w.lower() for w in words]

        term_freq = Counter(term_list)
        doc_term_counts[doc_id] = term_freq
        total_terms_per_doc[doc_id] = sum(term_freq.values())

    return doc_term_counts, total_terms_per_doc

def save_tfidf(tf_dict, idf_dict, total_terms, output_dir):
    for doc_id in tf_dict:
        out_path = os.path.join(output_dir, f"tfidf_page_{doc_id}.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            for term in tf_dict[doc_id]:
                tf = tf_dict[doc_id][term] / total_terms[doc_id]
                idf = idf_dict.get(term, 0)
                tfidf = tf * idf
                f.write(f"{term} {idf:.5f} {tfidf:.5f}\n")

def main():
    token_counts, token_totals = process_documents(TOKEN_DIR, is_lemma=False)
    token_idf = compute_idf(token_counts, len(token_counts))
    save_tfidf(token_counts, token_idf, token_totals, OUT_TOKENS_DIR)

    lemma_counts, lemma_totals = process_documents(LEMMA_DIR, is_lemma=True)
    lemma_idf = compute_idf(lemma_counts, len(lemma_counts))
    save_tfidf(lemma_counts, lemma_idf, lemma_totals, OUT_LEMMAS_DIR)


if __name__ == "__main__":
    main()
