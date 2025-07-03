import spacy
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from .variables import tech_skills

def preprocessing_logic(json_path):

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        text = data.get('extracted_text', '')


    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    clean_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    locations = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]

    cleaned_locations = [loc for loc in locations if loc.lower() not in tech_skills]

    data["locations"] = cleaned_locations
    data['tokens'] = clean_tokens

    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

