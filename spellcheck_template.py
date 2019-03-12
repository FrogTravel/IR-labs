import re
import nltk


def build_dictionary(documents):
    """
    Build dictionary of original word forms (without stemming, but tokenized, lowercased, and only apt words considered)
    :param documents: dict of documents (contents)
    :return: {'word1': freq_word1, 'word2': freq_word2, ...}

    """
    # TODO write your code here


def build_k_gram_index(dictionary, k):
    """
    Build index of k-grams for dictionary words. Padd with '$' ($word$) before splitting to k-grams
    :param dictionary: dictionary of original words
    :param k: number of symbols in one gram
    :return: {'gram1': ['word1_with_gram1', 'word2_with_gram1', ...],
              'gram2': ['word1_with_gram2', 'word2_with_gram2', ...], ...}
    """
    kgrams = {}
    for dict_word in dictionary:
        word = '$' + dict_word + '$'
        for index in range(k, len(word) + 1):
            key = word[index - k:index]
            if key in kgrams.keys():
                kgrams[word[index - k:index]] += [dict_word]
            else:
                kgrams[word[index - k:index]] = [dict_word]

    return kgrams


def generate_wildcard_options(wildcard, k_gram_index):
    """
    For a given wildcard return all words matching it using k-grams
    Refer to book chapter 3.2.2
    Don't forget to pad wildcard with '$', when appropriate
    :param wildcard: query word in a form of a wildcard
    :param k_gram_index:
    :return: list of options (matching words)
    """
    k = len(list(k_gram_index.keys())[0])  # TODO get size form k_gram_index
    wildcard_with_dollar = "$" + wildcard + "$"
    wildcards = wildcard_with_dollar.split("*")
    wildcard_kgram = []
    for part in wildcards:
        for index in range(k, len(part) + 1):
            k_gram = part[index - k:index]
            if len(k_gram) == k:
                wildcard_kgram.append(k_gram)

    sets = []
    for k_gram in wildcard_kgram:
        sets.append(set(k_gram_index[k_gram]))

    options = []
    for set_index in sets:
        options = sets[0].intersection(set_index)

    return list(options)


def produce_soundex_code(word):
    """
    Implement soundex algorithm, version from book chapter 3.4
    :param word: word in lowercase
    :return: soundex 4-character code, like 'k450'
    """
    code = word[:1]

    exception_letters = ['E', 'Y', 'U', 'I', 'O', 'A', 'H', 'W', 'e', 'y', 'u', 'i', 'o', 'a', 'h', 'w']

    cleaned_word = re.sub(r'[EYUIOAHWeyuioahw]', '', word)
    codes = {'B': '1', 'F': '1', 'P': '1', 'V': '1', 'b': '1', 'f': '1', 'p': '1', 'v': '1',
             'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2', 'c': '2', 'g': '2',
             'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
             'D': '3', 'T': '3', 'd': '3', 't': '3',
             'L': '4', 'l': '4',
             'M': '5', 'N': '5', 'm': '5', 'n': '5',
             'R': '6', 'r': '6'}
    first = 1
    if word[0] in exception_letters:
        first = 0

    for letter in cleaned_word[first:]:
        code += codes[letter]

    code = delete_redundant_letters(code)
    code = code[:4]

    if len(code) < 4:
        for index in range(0, 4 - len(code)):
            code += '0'
    return code


def build_soundex_index(dictionary):
    """
    Build soundex index for dictionary words.
    :param dictionary: dictionary of original words
    :return: {'code1': ['word1_with_code1', 'word'2'_with_code1', ...],
              'code2': ['word1_with_code2', 'word2_with_code2', ...], ...}
    """
    index = {}
    for word in dictionary:
        code = produce_soundex_code(word)
        if code in index.keys():
            index[code] += word
        else:
            index[code] = word

    return index


def delete_redundant_letters(word):
    result = word[0]
    for index, letter in enumerate(word[:-1]):
        if letter != word[index + 1]:
            result += word[index + 1]

    return result
