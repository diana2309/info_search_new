import os
import re
import pymorphy2
import nltk
from collections import defaultdict
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")
nltk.download("omw-1.4")

# Инициализация
morph = pymorphy2.MorphAnalyzer()
lemmatizer = WordNetLemmatizer()

# Папка с текстовыми файлами статей
ARTICLES_FOLDER = "downloaded_pages"

# Папки для сохранения результатов
TOKENS_FOLDER = "tokens"
LEMMAS_FOLDER = "lemmas"

# Создаём папки
os.makedirs(TOKENS_FOLDER, exist_ok=True)
os.makedirs(LEMMAS_FOLDER, exist_ok=True)

# Русские и английские слова (союзы, предлоги + слова из кода)
STOPWORDS = {
    "и", "в", "во", "на", "с", "по", "за", "от", "до", "у", "о", "а", "но", "же", "что", "как", "бы", "это",
    "the", "a", "an", "and", "or", "but", "if", "then", "else", "because", "so", "than", "after", "before",
    "of", "at", "in", "on", "by", "with", "about", "against", "between", "into", "through", "during",
    "before", "after", "above", "below", "to", "from", "up", "down", "under", "over", "again", "further",
    "function", "return", "var", "let", "const", "document", "window", "onclick", "getelementbyid",
    "getelementsbytagname", "script", "google", "console", "log", "alert", "addeventlistener"
}

# Функция очистки текста от HTML и JS-кода
def clean_text(text):
    text = re.sub(r"<[^>]+>", " ", text)  # Убираем HTML-теги
    text = re.sub(r"(?i)\b(function|var|let|const|return|document|window|onclick|script|console|log|alert)\b", " ", text)  # Убираем JS-код
    text = re.sub(r"[^\w\s]", " ", text)  # Убираем пунктуацию
    text = re.sub(r"\d+", "", text)  # Убираем числа
    text = text.lower().strip()  # Приводим к нижнему регистру и удаляем пробелы
    return text

# Функция фильтрации токенов
def is_valid_token(token):
    if len(token) > 20:
        return False
    if len(token) == 1:  # Однобуквенные слова
        return False
    if "_" in token:  # Слова с нижним подчеркиванием
        return False
    if re.search(r"(.)\1{4,}", token):  # Повторяющиеся символы
        return False
    if "amp" in token or "lt" in token or "gt" in token:
        return False
    return True

# Функция для токенизации текста
def tokenize(text):
    words = text.split()
    words = [word for word in words if word not in STOPWORDS and is_valid_token(word)]  # Фильтрация
    return set(words)  # Убираем дубликаты

# Функция определения языка слова
def is_russian(word):
    return re.match(r"^[а-яё]+$", word) is not None  # Проверяем, содержит ли слово только русские буквы

# Функция лемматизации для русского и английского языка
def lemmatize(word):
    if is_russian(word):
        return morph.parse(word)[0].normal_form  # Лемматизация русского слова
    else:
        return lemmatizer.lemmatize(word)  # Лемматизация английского слова

# Читаем статьи и обрабатываем их по отдельности
for filename in os.listdir(ARTICLES_FOLDER):
    if filename.endswith(".txt"):
        file_path = os.path.join(ARTICLES_FOLDER, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            text = clean_text(text)
            tokens = tokenize(text)

            # Группируем токены по леммам
            lemma_dict = defaultdict(set)
            for token in tokens:
                lemma = lemmatize(token)
                lemma_dict[lemma].add(token)

        # Пути для сохранения файлов
        tokens_path = os.path.join(TOKENS_FOLDER, f"tokens_{filename}")
        lemmas_path = os.path.join(LEMMAS_FOLDER, f"lemmas_{filename}")

        # Сохраняем токены
        with open(tokens_path, "w", encoding="utf-8") as token_file:
            token_file.write("\n".join(sorted(tokens)))

        # Сохраняем леммы в нужном формате
        with open(lemmas_path, "w", encoding="utf-8") as lemma_file:
            for lemma, token_set in sorted(lemma_dict.items()):
                lemma_file.write(f"{lemma} {' '.join(sorted(token_set))}\n")

print("Все файлы обработаны!")
