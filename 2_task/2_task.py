import os
import re
from collections import defaultdict, Counter
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# Папка с текстовыми файлами статей
ARTICLES_FOLDER = "downloaded_pages"

# Русские стоп-слова
STOPWORDS = {"и", "в", "во", "на", "с", "по", "за", "от", "до", "у", "о", "а", "но", "же", "что", "как", "бы", "это"}

# Функция очистки текста от HTML-тегов
def clean_text(text):
    text = re.sub(r"<[^>]+>", " ", text)  # Убираем HTML-теги
    text = re.sub(r"[^\w\s]", " ", text)  # Убираем пунктуацию
    text = re.sub(r"\d+", "", text)  # Убираем числа
    text = text.lower().strip()  # Приводим к нижнему регистру и удаляем пробелы
    return text

# Функция фильтрации мусорных токенов
def is_valid_token(token):
    if len(token) > 20:
        return False
    if len(token) == 1:  # Однобуквенные слова (и русские, и английские)
        return False
    if "_" in token:  # Слова с нижним подчеркиванием
        return False
    if re.search(r"(.)\1{4,}", token):
        return False
    if "amp" in token or "lt" in token or "gt" in token:
        return False
    return True

# Функция для токенизации текста
def tokenize(text):
    words = text.split()
    words = [word for word in words if word not in STOPWORDS and is_valid_token(word)]  # Убираем стоп-слова и мусор
    return set(words)  # Убираем дубликаты


def lemmatize(word):
    parsed = morph.parse(word)[0]
    lemma = parsed.normal_form  # Основная форма слова
    lang = "ru" if "LATN" not in parsed.tag else "en"  # Определение языка (русский/английский)
    return lemma, lang

# Читаем статьи и собираем токены
all_tokens = set()
lemma_dict = defaultdict(set)
lemma_counter = Counter()

for filename in os.listdir(ARTICLES_FOLDER):
    if filename.endswith(".txt"):
        with open(os.path.join(ARTICLES_FOLDER, filename), "r", encoding="utf-8") as file:
            text = file.read()
            text = clean_text(text)
            tokens = tokenize(text)
            all_tokens.update(tokens)
            for token in tokens:
                lemma, lang = lemmatize(token)
                lemma_dict[(lemma, lang)].add(token)
                lemma_counter[(lemma, lang)] += 1

# Фильтруем леммы:
filtered_lemmas = {
    lemma: words
    for (lemma, lang), words in lemma_dict.items()
    if len(words) > 1 or lemma_counter[(lemma, lang)] > 1  # Если более 1 формы или слово встречается >1 раза
}

# Сохраняем токены в файл
with open("tokens.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(sorted(all_tokens)))

# Сохраняем леммы в файл
with open("lemmas.txt", "w", encoding="utf-8") as file:
    for lemma, words in sorted(filtered_lemmas.items()):
        file.write(f"{lemma}: {', '.join(sorted(words))}\n")

print("Токены и леммы сохранены!")
