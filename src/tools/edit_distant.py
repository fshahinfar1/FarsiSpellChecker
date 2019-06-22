from ..constants import ALPHABET


def edit_ditance(w1, w2):
    l1 = len(w1)
    l2 = len(w2)
    dp = [[j for j in range(l2 + 1)] for i in range(l1 + 1)]
    for i in range(l1 + 1):
        dp[i][0] = i
    for i in range(1, l1 + 1):
        for j in range(1, l2 + 1):
            delete = dp[i-1][j]
            insert = dp[i][j-1]
            substitude = dp[i-1][j-1] if w1[i-1] == w2[j-1] else dp[i-1][j-1]+1
            dp[i][j] = min(delete, insert, substitude) 
    return dp[l1][l2]


def generate_all_edist_words(word, dist):
    """
    generate all words with edit distance of `dist`
    1) replace with new chars
    2) remove a char
    3) insert a char
    """
    length = len(word)
    if length < dist:
        return generate_all_edist_words(word, length)
    if dist == 1:
        result = list()
        # substitude a character of word with `ch`
        for ch in ALPHABET:
            tmp = [list(word) for i in range(length)]
            for i in range(length):
                tmp[i][i] = ch
            tmp = [''.join(x) for x in tmp]
            result += tmp
        # remove a char
        for i in range(length):
            result.append(word[:i]+word[i+1:])
        # insert a char
        for ch in ALPHABET:
            for i in range(length):
                result.append(word[:i]+ch+word[i:])
        return set(result)
    else:
        prev_res = generate_all_edist_words(word, dist - 1)
        result = set()
        for item in prev_res:
            tmp = generate_all_edist_words(item, 1)
            result.update(tmp)
        return result

