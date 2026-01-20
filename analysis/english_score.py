
COMMON_WORDS = {
    "THE","AND","TO","OF","IN","IT","IS","BE","AS","AT","SO","WE","HE",
    "BY","OR","ON","DO","IF","ME","MY","YOU","ARE","FOR","WITH","THIS"
}
ETAOIN = "ETAOINSHRDLU"
def score_english(text: str) -> float:
    if not text:
        return 0.0
    T = text.upper()
    base = sum(ch.isalpha() or ch == ' ' for ch in T) / len(T)
    words = [w for w in ''.join(ch if ch.isalpha() or ch==' ' else ' ' for ch in T).split() if w]
    word_bonus = 0
    for w in words:
        if w in COMMON_WORDS:
            word_bonus += 1
    word_bonus = word_bonus / max(1, len(words))
    counts = {ch: 0 for ch in ETAOIN}
    for ch in T:
        if ch in counts:
            counts[ch] += 1
    freq_bonus = sum(counts.values()) / max(1, len(T))
    return 0.6 * base + 0.25 * freq_bonus + 0.15 * word_bonus 