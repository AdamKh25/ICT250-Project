
def isEnglish(s):
    s = s.upper()
    common = [' THE ', ' AND ', ' TO ', ' OF ', ' IN ', ' IS ', ' IT ', ' YOU ', ' FOR ', ' WITH ']
    score = sum(s.count(w) for w in common) * 3
    score += s.count(' ')
    letters = sum(ch.isalpha() for ch in s)
    score += 0.02 * letters
    return score >= 2.5  # crude threshold; tune as needed
def score_english(s):
    # expose a score for ranking hacks
    s = s.upper()
    common = [' THE ', ' AND ', ' TO ', ' OF ', ' IN ', ' IS ', ' IT ', ' YOU ', ' FOR ', ' WITH ']
    return sum(s.count(w) for w in common) * 3 + s.count(' ') + 0.02 * sum(ch.isalpha() for ch in s)
