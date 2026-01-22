# check if text looks like english
def isEnglish(s):
    # convert text to uppercase
    s = s.upper()

    # common english word patterns
    common = [' THE ', ' AND ', ' TO ', ' OF ', ' IN ', ' IS ', ' IT ', ' YOU ', ' FOR ', ' WITH ']

    # score based on common words
    score = sum(s.count(w) for w in common) * 3

    # add score for spaces
    score += s.count(' ')

    # count alphabetic characters
    letters = sum(ch.isalpha() for ch in s)

    # add small weight for letter count
    score += 0.02 * letters

    # return true if score passes threshold
    return score >= 2.5  


# compute english score for text
def score_english(s):
    # convert text to uppercase
    s = s.upper()

    # common english word patterns
    common = [' THE ', ' AND ', ' TO ', ' OF ', ' IN ', ' IS ', ' IT ', ' YOU ', ' FOR ', ' WITH ']

    # calculate total score
    return (
        sum(s.count(w) for w in common) * 3 +
        s.count(' ') +
        0.02 * sum(ch.isalpha() for ch in s)
    )
