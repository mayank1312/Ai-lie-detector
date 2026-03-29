import wikipedia

def get_wikipedia_context(query):
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except:
        return "No relevant information found."