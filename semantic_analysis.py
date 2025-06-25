import spacy
from rake_nltk import Rake
from transformers import pipeline
import re

# Load models
nlp = spacy.load("en_core_web_md")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_metadata(text):
    # Clean text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Keyphrase extraction
    r = Rake()
    r.extract_keywords_from_text(text)
    keyphrases = r.get_ranked_phrases()[:5]
    
    # Entity recognition
    doc = nlp(text)
    entities = {ent.text: ent.label_ for ent in doc.ents}
    
    # Summary generation
    if len(text.split()) > 100:
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    else:
        summary = text[:500] + "..." if len(text) > 500 else text
    
    # Document stats
    word_count = len(text.split())
    sentence_count = len(list(doc.sents))
    
    return {
        "keyphrases": keyphrases,
        "entities": entities,
        "summary": summary,
        "document_stats": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "readability": "Technical" if word_count/sentence_count > 20 else "Standard"
        }
    }
