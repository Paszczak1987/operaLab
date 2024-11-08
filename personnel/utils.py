import unicodedata

def remove_diacritical_marks(text):
    normalized_text = ""
    for char in text:
        if char != "ß":
            try:
                char_name = unicodedata.name(char).split()
                normalized_text += unicodedata.lookup(' '.join(char_name[:4]))
            except ValueError:
                normalized_text += char
        else:
            normalized_text += 's'
    return normalized_text

