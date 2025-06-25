import spacy
from rake_nltk import Rake
from transformers import pipeline
import re

# Load models once
nlp = spacy.load("en_core_web_md")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def extract_keyphrases(text: str, num_phrases=5):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:num_phrases]

def extract_entities(text: str):
    doc = nlp(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

def summarize_text(text: str):
    # Summarize only if text is long enough
    if len(text.split()) < 50:
        return text
    return summarizer(text, max_length=120, min_length=30, do_sample=False)[0]['summary_text']

def analyze_sentiment(text: str):
    # Simple sentiment analysis using spaCy
    doc = nlp(text)
    pos = sum(1 for token in doc if token.pos_ == "ADJ" and token.sentiment > 0)
    neg = sum(1 for token in doc if token.pos_ == "ADJ" and token.sentiment < 0)
    if pos > neg:
        return "Positive"
    elif neg > pos:
        return "Negative"
    else:
        return "Neutral"

def analyze_readability(text: str):
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    try:
        avg = len(words) / max(1, len(sentences))
        return "Technical" if avg > 20 else "Standard"
    except Exception:
        return "Unknown"

def generate_metadata(text: str) -> dict:
    text = clean_text(text)
    return {
        "keyphrases": extract_keyphrases(text),
        "entities": extract_entities(text),
        "summary": summarize_text(text),
        "sentiment": analyze_sentiment(text),
        "readability": analyze_readability(text),
        "stats": {
            "word_count": len(text.split()),
            "char_count": len(text)
        }
    }
