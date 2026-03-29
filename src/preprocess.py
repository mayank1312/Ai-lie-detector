import string

def clean_text(text):
    
    text = str(text).lower()
    
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text