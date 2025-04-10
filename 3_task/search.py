import json
import re

# Загружаем индекс
with open('inverted_index.json', 'r', encoding='utf-8') as f:
    INDEX = json.load(f)

ALL_DOCS = set()
for doc_ids in INDEX.values():
    ALL_DOCS.update(doc_ids)


def get_docs(term):
    return set(INDEX.get(term.lower(), []))


def parse_query(query):
    query = query.replace("(", " ( ").replace(")", " ) ")
    return query.split()


def eval_query(tokens):
    def helper(tokens):
        stack = []
        while tokens:
            token = tokens.pop(0)
            if token == '(':
                stack.append(helper(tokens))
            elif token == ')':
                break
            elif token.upper() in {'AND', 'OR', 'NOT'}:
                stack.append(token.upper())
            else:
                stack.append(get_docs(token))

        # Обработка NOT сначала
        while 'NOT' in stack:
            i = stack.index('NOT')
            negated = ALL_DOCS - stack[i + 1]
            stack = stack[:i] + [negated] + stack[i + 2:]

        # Затем AND
        while 'AND' in stack:
            i = stack.index('AND')
            result = stack[i - 1] & stack[i + 1]
            stack = stack[:i - 1] + [result] + stack[i + 2:]

        # Затем OR
        while 'OR' in stack:
            i = stack.index('OR')
            result = stack[i - 1] | stack[i + 1]
            stack = stack[:i - 1] + [result] + stack[i + 2:]

        return stack[0]

    return helper(tokens)


def search(query):
    tokens = parse_query(query)
    result = eval_query(tokens)
    return sorted(result)


if __name__ == "__main__":
    while True:
        query = input("Введите булев запрос: ")
        if query.lower() in {"exit", "quit"}:
            break
        result = search(query)
        print("Найдены документы:", result)
