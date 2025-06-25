import re
import spacy
from keybert import KeyBERT
from transformers import pipeline
from datetime import datetime
import nltk
from dateutil.parser import parse

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
    """Improved title extraction with section detection"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    # Prioritize lines before abstract/introduction
    for i, line in enumerate(lines):
        if "abstract" in line.lower() or "introduction" in line.lower():
            if i > 0 and 10 <= len(lines[i-1]) <= 120:
                return lines[i-1]
    # Fallback to first meaningful line
    for line in lines:
        if 10 <= len(line) <= 120 and not line.isupper():
            return line
    return "Untitled Document"

def extract_author(text):
    """Enhanced author extraction with multiple heuristics"""
    # Try author line pattern (Name - Title/affiliation)
    author_pattern = r'^([A-Z][a-z]+(?:\s[A-Z][a-z]*)+)\s*-\s*[A-Za-z\s]+$'
    lines = text.split('\n')
    for line in lines[:20]:  # Check first 20 lines
        match = re.match(author_pattern, line)
        if match:
            return match.group(1).strip()
    
    # NER with context filtering
    doc = nlp(text[:3000])
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if persons:
        # Filter out common non-author names
        author_candidates = [p for p in persons if not any(word in p.lower() for word in ['university', 'department', 'institute'])]
        if author_candidates:
            return author_candidates[0]
    
    # "By" pattern detection
    match = re.search(r"(?i)(?:by|author|written by)[: ]+\s*([\w\s\.\-']+)", text[:2000])
    if match:
        return match.group(1).strip().title()
    
    return "Unknown Author"

def extract_date(text):
    """Robust date extraction with context awareness"""
    # Find 4-digit years in context
    year_matches = re.findall(r'\b(19[7-9][0-9]|20[0-2][0-9])\b', text)
    if year_matches:
        return max(year_matches)  # Most recent year
    
    # NER with date filtering
    doc = nlp(text[:5000])
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE" 
             and re.search(r'\b(19|20)\d{2}\b', ent.text)]
    
    if dates:
        try:
            # Parse and return most plausible date
            parsed_dates = [parse(d, fuzzy=True) for d in dates]
            valid_dates = [d for d in parsed_dates if 1900 <= d.year <= datetime.now().year + 1]
            if valid_dates:
                return max(valid_dates).strftime("%Y")
        except:
            pass
    
    return "Not found"

def extract_keyphrases(text):
    return [kw[0] for kw in kw_model.extract_keywords(
        text, 
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=7
    )]

def map_topics(keyphrases):
    topics = set()
    for topic, keywords in TOPIC_MAP.items():
        if any(kw in phrase.lower() for phrase in keyphrases for kw in keywords):
            topics.add(topic)
    return list(topics) or ["General"]

def analyze_sentiment(text):
    doc = nlp(text)
    pos = sum(1 for token in doc if token.sentiment > 0)
    neg = sum(1 for token in doc if token.sentiment < 0)
    return "Positive" if pos > neg else "Negative" if neg > pos else "Neutral"

def analyze_readability(text):
    words = text.split()
    sentences = [s for s in re.split(r'[.!?]', text) if s.strip()]
    if not sentences: 
        return "Unknown"
    avg = len(words) / len(sentences)
    return "Technical" if avg > 25 else "Standard"

def generate_summary(text):
    if len(text.split()) < 100: 
        return "Document too short for meaningful summary"
    return summarizer(text[:4100], max_length=150, min_length=30)[0]['summary_text']

def generate_metadata(text):
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
