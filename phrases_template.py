import nltk


def find_ngrams_PMI(tokenized_text, freq_thresh, pmi_thresh, n):
    """
    Finds n-grams in tokenized text, limiting by frequency and pmi value
    :param tokeniz
    ,1ed_text: list of tokens
    :param freq_thresh: number, only consider ngrams more frequent than this threshold
    :param pmi_thresh: number, only consider ngrams that have pmi value greater than this threshold
    :param n: length of ngrams to consider, can be 2 or 3
    :return: set of ngrams tuples - {('ngram1_1', 'ngram1_2'), ('ngram2_1', 'ngram2_2'), ... }
    """
    if n == 2: # might be only 2 or 3
        measure = nltk.collocations.BigramAssocMeasures
        finder = nltk.collocations.BigramCollocationFinder
    else:
        measure = nltk.collocations.TrigramAssocMeasures
        finder = nltk.collocations.TrigramAssocMeasures

    words = finder.from_words(tokenized_text)
    words.apply_freq_filter(freq_thresh) # Отфильтровали
    print(words)




def build_ngram_index(tokenized_documents, ngrams):
    """
    Builds index based on ngrams and collection of tokenized docs
    :param tokenized_documents: {doc1_id: ['token1', 'token2', ...], doc2_id: ['token1', 'token2', ...]}
    :param ngrams: set of ngrams tuples - {('ngram1_1', 'ngram1_2'), ('ngram2_1', 'ngram2_2', 'ngram2_3'), ... }
    :return: dictionary - {ngram_tuple :[ngram_tuple_frequency, (doc_id_1, doc_freq_1), (doc_id_2, doc_freq_2), ...], ...}
    """
    # TODO write your code here


def main():
    tokenized_text = ['on', 'saturday', ',', 'huge', 'numbers', 'of', 'venezuelans', 'took', 'to', 'the', 'streets',
                      '—', 'most', 'of', 'them', 'to', 'show', 'their', 'support', 'for', 'opposition', 'leader',
                      'juan', 'guaidó', '.', 'a', 'smaller', 'contingency', 'came', 'out', 'in', 'support', 'of',
                      'president', 'nicolás', 'maduro', ',', 'to', 'celebrate', 'the', '20th', 'anniversary', 'of',
                      'the', 'rise', 'to', 'power', 'of', 'his', 'predecessor', ',', 'hugo', 'chávez', '.', 'scenes',
                      'from', 'the', 'two', 'sides', 'illustrate', 'the', 'deep', 'divisions', 'that', 'have',
                      'emerged', 'in', 'venezuela', 'in', 'recent', 'weeks', ',', 'after', 'guaidó', 'declared',
                      'himself', 'interim', 'president', 'and', 'maduro', 'refused', 'to', 'step', 'down', '.',
                      'marches', 'in', 'support', 'of', 'guaidó', ',', 'the', '35-year-old', 'head', 'of', 'the',
                      'opposition-controlled', 'national', 'assembly', ',', 'appear', 'to', 'have', 'attracted',
                      'massive', 'crowds', 'of', 'demonstrators', '—', 'holding', 'signs', 'calling', 'for', 'fair',
                      'elections', 'and', 'sovereign', 'democracy', '—', 'in', 'caracas', 'and', 'other', 'cities',
                      'around', 'the', 'country', '.', 'in', 'recent', 'years', ',', 'venezuela', 'has', 'been',
                      'submerged', 'in', 'a', 'state', 'of', 'political', 'and', 'humanitarian', 'turmoil', '.',
                      'millions', 'fled', 'the', 'country', 'as', 'migrants', 'and', 'refugees', ',', 'escaping',
                      'hyperinflation', 'that', 'made', 'the', 'costs', 'of', 'basic', 'goods', 'soar', '.', 'the',
                      'country', '’', 's', 'health', 'system', 'has', 'also', 'disintegrated', '.', 'when', 'guaidó',
                      'declared', 'himself', 'interim', 'president', ',', 'the', 'united', 'states', 'quickly', 'threw',
                      'its', 'support', 'behind', 'him', '.', 'in', 'venezuela', ',', 'maduro', 'still', 'has', 'the',
                      'support', 'of', 'the', 'military', '.', 'but', 'early', 'on', 'saturday', ',', 'just', 'before',
                      'the', 'planned', 'demonstrations', ',', 'an', 'acting', 'venezuelan', 'air', 'force', 'general',
                      'switched', 'sides', ',', 'throwing', 'his', 'support', 'behind', 'guaidó', 'in', 'a', 'widely',
                      'circulated', 'video', 'on', 'social', 'media', '.', 'in', 'the', 'short', 'clip', ',', 'he',
                      'says', 'that', '“', '90', 'percent', 'of', 'the', 'armed', 'forces', 'are', 'not', 'with', 'the',
                      'dictator.', '”', 'the', 'venezuelan', 'air', 'force', 'responded', 'on', 'twitter', ',',
                      'calling', 'the', 'general', 'a', 'traitor', 'and', 'claiming', 'he', '“', 'has', 'no',
                      'leadership', 'at', 'the', 'air', 'force.', '”', 'these', 'photos', 'offer', 'a', 'glimpse',
                      'into', 'what', 'the', 'demonstrations', 'look', 'like', '.']

    find_ngrams_PMI(tokenized_text, 2, 6, 2)

if __name__ == "__main__":
    main()
