import re
import spacy
from keybert import KeyBERT
from transformers import pipeline
from datetime import datetime
import nltk

# Ensure NLTK resources are available
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')

# Load spaCy model with direct import
try:
    import en_core_web_md
    nlp = en_core_web_md.load()
except ImportError:
    # Fallback for local environments
    from spacy.cli import download
    download("en_core_web_md")
    import en_core_web_md
    nlp = en_core_web_md.load()
kw_model = KeyBERT()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Predefined topics mapping
TOPIC_MAP = {
    "Technology": ["ai", "data", "cloud", "algorithm", "software", "digital", "blockchain"],
    "Finance": ["loan", "investment", "stock", "bank", "equity", "credit", "capital"],
    "Healthcare": ["health", "medical", "patient", "disease", "hospital", "treatment"],
    "Education": ["school", "student", "learning", "university", "course", "teacher"],
    "Environment": ["climate", "sustainability", "energy", "conservation", "pollution"],
    "Government": ["policy", "regulation", "public", "government", "law", "administration"]
}

def extract_title(text):
    """Extract document title using heuristic rules"""
    # First non-empty line
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        candidate = lines[0]
        if 10 <= len(candidate) <= 120 and not candidate.isupper():
            return candidate
    
    # First sentence
    first_sentence = text.split('.')[0]
    if 20 <= len(first_sentence) <= 150:
        return first_sentence
    
    return "Untitled Document"

def extract_author(text):
    """Extract author using NER and heuristics"""
    doc = nlp(text[:2000])  # Only scan beginning
    
    # Find persons in document
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if persons:
        return persons[0]
    
    # Look for "by" patterns
    match = re.search(r"(?i)(?:by|author|written by)[: ]+\s*(\w+ \w+)", text[:1000])
    if match:
        return match.group(1).title()
    
    return "Unknown Author"

def extract_date(text):
    """Find dates in document"""
    doc = nlp(text[:5000])  # Only scan beginning
    
    # Find dates in document
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    if dates:
        return dates[0]
    
    # Current year as fallback
    return datetime.now().strftime("%Y")

def extract_keyphrases(text):
    """Extract key phrases using KeyBERT"""
    return [kw[0] for kw in kw_model.extract_keywords(
        text, 
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=7
    )]

def map_topics(keyphrases):
    """Map keyphrases to predefined topics"""
    topics = set()
    for topic, keywords in TOPIC_MAP.items():
        if any(kw in phrase.lower() for phrase in keyphrases for kw in keywords):
            topics.add(topic)
    return list(topics) or ["General"]

def analyze_sentiment(text):
    """Simple sentiment analysis"""
    doc = nlp(text)
    positive = sum(1 for token in doc if token.sentiment > 0)
    negative = sum(1 for token in doc if token.sentiment < 0)
    return "Positive" if positive > negative else "Negative" if negative > positive else "Neutral"

def analyze_readability(text):
    """Classify document readability"""
    words = text.split()
    sentences = [s for s in re.split(r'[.!?]', text) if s.strip()]
    
    if not sentences:
        return "Unknown"
    
    avg_sentence_length = len(words) / len(sentences)
    return "Technical" if avg_sentence_length > 25 else "Standard"

def generate_summary(text):
    """Generate abstractive summary"""
    if len(text.split()) < 100:
        return "Document too short for meaningful summary"
    
    # Use first 1024 tokens for summarization
    inputs = text[:4100]
    return summarizer(inputs, max_length=150, min_length=30)[0]['summary_text']

def generate_metadata(text):
    """Main metadata generation function"""
    return {
        "title": extract_title(text),
        "author": extract_author(text),
        "date": extract_date(text),
        "keyphrases": extract_keyphrases(text),
        "topics": map_topics(extract_keyphrases(text)),
        "summary": generate_summary(text),
        "sentiment": analyze_sentiment(text),
        "readability": analyze_readability(text),
        "stats": {
            "word_count": len(text.split()),
            "char_count": len(text),
            "sentence_count": len([s for s in re.split(r'[.!?]', text) if s.strip()])
        }
    }
