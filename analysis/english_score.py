import string

COMMON_WORDS = {
    "THE","AND","TO","OF","IN","IS","YOU","THAT","IT","HE","WAS","FOR","ON","ARE","AS",
    "WITH","HIS","THEY","I","AT","BE","THIS","HAVE","FROM","OR","ONE","HAD","BY","WORD",
}

def score_english(text: str) -> float:
    if not text:
        return 0.0

    t = text.upper()
    letters = sum(ch in string.ascii_uppercase for ch in t)
    spaces = t.count(" ")
    printable = sum(32 <= ord(ch) <= 126 or ch in "\n\r\t" for ch in text)

    if printable / max(1, len(text)) < 0.9:
        return 0.0

    score = spaces * 1.5

    words = [w.strip(string.punctuation) for w in t.split()]
    hits = sum(1 for w in words if w in COMMON_WORDS)
    score += hits * 10.0
    score += (letters / max(1, len(t))) * 5.0

    return score

