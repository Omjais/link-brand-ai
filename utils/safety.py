BAD_WORDS = {"spammy","fake","scam","hate","violence"}

def check(text: str) -> list[str]:
    hits = []
    lower = text.lower()
    for w in BAD_WORDS:
        if w in lower:
            hits.append(w)
    return hits
