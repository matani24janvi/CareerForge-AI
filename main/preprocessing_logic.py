import nltk
import json
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocessing_logic(json_path):

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        text = data.get('extracted_text', '')


    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    clean_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]


    data['tokens'] = clean_tokens

    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

