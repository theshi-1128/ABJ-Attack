def clean_text(text):
    """Remove line breaks from text"""
    return text.replace("\r", "").replace("\n", "")