from glob import glob
import nltk
from bs4 import BeautifulSoup
import pickle
from collections import Counter
import math
import heapq
import re
import os
import fileinput

stop_words = {'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its',
              'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with'}
ps = nltk.stem.PorterStemmer()


# tokenize text using nltk lib
def tokenize(text):
    return nltk.word_tokenize(text)


# stem word using provided stemmer
def stem(word, stemmer):
    return stemmer.stem(word)


# checks if word is appropriate - not a stop word and isalpha
def is_apt_word(word):
    return word not in stop_words and word.isalpha()


# combines all previous methods together
def preprocess(text):
    tokenized = tokenize(text.lower())
    return [stem(w, ps) for w in tokenized if is_apt_word(w)]


def build_index(path, limit=None):
    """
    # principal function - builds an index of terms in all documents
    # generates 3 dictionaries and saves on disk as separate files:
    # index - term:[term_frequency, (doc_id_1, doc_freq_1), (doc_id_2, doc_freq_2), ...]
    # doc_lengths - doc_id:doc_length
    # documents - doc_id: doc_content_clean
    :param path: path to directory with original reuters files
    :param limit: number of articles to process, for testing. If limit is not None,
                  return index when done, without writing files to disk
    """
    """
     tokenization, removing stop words, stemming/lemmatization
     lemmatization instead of stemming
     title (if any) + ‘\n’ + body of an article (if any).
     
     <reuters></reuters> // границы между документами
     
     document lengths(number of terms after preprocessing)
     documents themselves  i.e. article contents
    """
    # filenames = glob(path + 'reut2-0**.sgm')
    # for file in fileinput.input(filenames):
    #     soup = BeautifulSoup(file, "html.parser")
    #     articles = soup.find_all('REUTERS')
    #     print(articles)

    # for filename in os.listdir(path):
    #     if filename.startswith("reut2-0"):
    #         with open("{}/{}".format(path, filename), 'r') as f:
    #             soup = BeautifulSoup(f, "html.parser")
    #             articles = soup.find_all('REUTERS')
    #             print(articles)
    term = {}  # term: []

    filenames = sorted(glob(path + 'reut2-0**.sgm'))

    doc_lengths = {}

    doc_content = {}
    counter = 0
    for f in filenames:
        # Чтение файлов
        reuter_stream = open(f, encoding="latin-1")
        reuter_content = reuter_stream.read()
        soup = BeautifulSoup(reuter_content, "html.parser")
        articles = soup.find_all('reuters')

        for article in articles:
            # Нормализация
            # text = article.body.string
            # text.replace('\n', ' ')
            #
            # for word in text.split(' '): # Для каждого слова в article
            #

            # Индексирование
            try:
                if limit is not None and counter == limit:
                    break
                title, body = get_article(article)
                text = title + '\n' + body

                doc_content[int(article['newid'])] = text

                preprocessed_text = preprocess(text)
                index_article(preprocessed_text, term, article)

                doc_lengths[int(article['newid'])] = len(preprocessed_text)
                counter += 1
            except AttributeError:  # TODO уменьшить exception
                pass
        if limit is not None and counter == limit:
            break

    reuters_index_file = open("reuters_index.p", "wb")
    pickle.dump(term, reuters_index_file)
    reuters_index_file.close()

    reuters_doc_lengths_file = open("reuters_doc_lengths.p", "wb")
    pickle.dump(doc_lengths, reuters_doc_lengths_file)
    # reuters_doc_lengths_file.write(str(doc_lengths))
    reuters_doc_lengths_file.close()

    reuters_documents_file = open("reuters_documents.p", "wb")
    pickle.dump(doc_content, reuters_documents_file)
    # reuters_documents_file.write(str(doc_content))
    reuters_documents_file.close()

    return term


def get_article(text):
    title = ""
    body = ""
    try:
        title = text.title.string
    except AttributeError:
        print("no TITLE: " + text['newid'])

    try:
        body = text.body.string
    except AttributeError:
        print("No BODY : " + text['newid'])

    if title == "" and body == "":
        raise AttributeError
    return title, body


def index_article(text, term, article):
    # text = article.body.string # TODO standalone method for tokenization with throwing away some characters
    # Throw away punctuation characters, stop_words
    # text.replace('\n', ' ')

    for word in text:
        if word not in stop_words:  # Если не стоп слово
            #  добавить терм [0, (doc_id, 1)]
            if word not in term.keys():  # Если нет в terms
                # [term_frequency, (doc_id, doc_freq), (doc_id, doc_freq), ...]
                term[word] = [1, (int(article['newid']), 1)]

            else:  # Если уже такой терм был
                term_array = term[word]
                term_array[0] += 1  # add 1 to frequency of term

                if term[word][len(term[word]) - 1][0] == int(article['newid']):
                    # Если тот же документ -> добавить doc_feq++
                    doc_tuple_id = len(term[word]) - 1
                    doc_id, doc_freq = term_array[doc_tuple_id]
                    doc_freq += 1
                    term_array[doc_tuple_id] = (doc_id, doc_freq)  # add one to frequency in specific doc
                else:  # Если другой документ -> добавить tuple (doc_id, doc_freq)
                    term_array.append((int(article['newid']), 1))


def cosine_scoring(query, doc_lengths, index):
    """
    Computes scores for all documents containing any of query terms
    according to the COSINESCORE(q) algorithm from the book (chapter 6)

    :param query: dictionary - term:frequency
    :return: dictionary of scores - doc_id:score
    """
    # TODO write your code here

    # for word in query:
    scores = dict()

    for term in query:
        if term in index:
            all_documents = index[term][1:]
            qtf = get_query_term_frequency(index, all_documents)
            for doc_id, doc_freq in all_documents:
                dtw = doc_freq * qtf
                if doc_id not in scores.keys():
                    scores[doc_id] = 0
                scores[doc_id] += query_weight(qtf, query[term]) * dtw

    normalization(doc_lengths, scores)

    return scores


def get_query_term_frequency(index, all_documents):
    return math.log(len(index) / len(all_documents), 10)


def query_weight(qtf, term):
    return term * qtf


def normalization(doc_lengths, scores):
    for document in doc_lengths:
        if document in scores:
            scores[document] = scores[document] / doc_lengths[document]
        else:
            scores[document] = 0


def okapi_scoring(query, doc_lengths, index, k1=1.2, b=0.75):
    """
    Computes scores for all documents containing any of query terms
    according to the Okapi BM25 ranking function, refer to wikipedia,
    but calculate IDF as described in chapter 6, using 10 as a base of log

    :param query: dictionary - term:frequency
    :return: dictionary of scores - doc_id:score
    """
    score_dict = {}
    for doc_name, doc_length in doc_lengths.items():
        score = 0
        for word in query:
            # idf = IDF(word, len(index.keys()), get_number_of_documents_with_word(word, index))
            idf = IDF(index, word, len(doc_lengths))
            term_frequency = get_term_frequency_in_document(word, index, doc_name)
            avgdl = sum(doc_lengths.values()) * 1.0 / len(doc_lengths)
            score += idf * ((term_frequency * (k1 + 1)) / (term_frequency + k1 * (1 - b + b * (doc_length / avgdl))))
        score_dict[doc_name] = score

    return score_dict


def get_number_of_documents_with_word(word, index):
    term_array = index[word]
    return len(term_array[1:])


def get_term_frequency_in_document(term, index, document_id):
    if term in index:
        for doc_id, doc_freq in index[term][1:]:
            if doc_id == document_id:
                return doc_freq
    return 0


def tfidf(index, term, documents, document_id):
    return tftd(index, term, document_id) * IDF(index, term, documents)


def tftd(index, term, document_id):
    for doc_id, doc_freq in index[term][1:]:
        if doc_id == document_id:
            return doc_freq
    return 0


def IDF(index, term, documents):
    try:
        return math.log10(documents / df(index, term))
    except:
        return 0


def df(index, term):
    l = index.get(term, [0])
    return len(l) - 1


def answer_query(raw_query, index, doc_lengths, documents, top_k, scoring_fnc):
    """
    :param raw_query: user query as it is
    :param top_k: how many results to show
    :param scoring_fnc: cosine/okapi
    :return: list of ids of retrieved documents (top_k)
    """
    # pre-process query the same way as documents
    query = preprocess(raw_query)
    # count frequency
    query = Counter(query)
    # retrieve all scores
    scores = scoring_fnc(query, doc_lengths, index)
    # put them in heapq data structure, to allow convenient extraction of top k elements
    h = []
    for doc_id in scores.keys():
        neg_score = -scores[doc_id]
        heapq.heappush(h, (neg_score, doc_id))
    # retrieve best matches
    top_k = min(top_k, len(h))  # handling the case when less than top k results are returned
    print('\033[1m\033[94mANSWERING TO:', raw_query, 'METHOD:', scoring_fnc.__name__, '\033[0m')
    print(top_k, "results retrieved")
    top_k_ids = []
    for k in range(top_k):
        best_so_far = heapq.heappop(h)
        top_k_ids.append(best_so_far)
        article = documents[best_so_far[1]]
        article_terms = tokenize(article)
        intersection = [t for t in article_terms if is_apt_word(t) and stem(t, ps) in query.keys()]
        for term in intersection:  # highlight terms for visual evaluation
            article = re.sub(r'(' + term + ')', r'\033[1m\033[91m\1\033[0m', article, flags=re.I)
        print("-------------------------------------------------------")
        print(article)

    return top_k_ids


def main():
    reuters_path = 'reuters21578/'
    if not os.path.isfile('reuters_index.p'):
        build_index(reuters_path)
    with open('reuters_index.p', 'rb') as fp:
        index = pickle.load(fp)
    with open('reuters_doc_lengths.p', 'rb') as fp:
        doc_lengths = pickle.load(fp)
    with open('reuters_documents.p', 'rb') as fp:
        documents = pickle.load(fp)
    answer_query("soviet union war afghanistan", index, doc_lengths, documents, 5, cosine_scoring)
    answer_query("soviet union war afghanistan", index, doc_lengths, documents, 5, okapi_scoring)

    answer_query("black monday", index, doc_lengths, documents, 5, cosine_scoring)
    answer_query("black monday", index, doc_lengths, documents, 5, okapi_scoring)

    answer_query("apple personal computer", index, doc_lengths, documents, 5, cosine_scoring)
    answer_query("apple personal computer", index, doc_lengths, documents, 5, okapi_scoring)

    # print(okapi_scoring(preprocess('Some query here'), doc_lengths, index))

    # query = Counter(preprocess("x y z"))
    # doc_lengths = {1: 20, 2: 15, 3: 10}
    # index = {'x': [2, (1, 1), (2, 1)], 'y': [2, (1, 1), (3, 1)], 'z': [1, (2, 1)]}

    # # test cosine_scores
    # from math import isclose
    # # test okapi_scores
    # okapi_scores = okapi_scoring(query, doc_lengths, index)
    # print(okapi_scores)
    # if okapi_scores[2] > okapi_scores[1] > okapi_scores[3] and isclose(okapi_scores[2], 0.653, abs_tol=1e-3):
    #     print("okapi_scores OK")
    # else:
    #     print("okapi_scores FAIL")
    #
    # cosine_scores = cosine_scoring(query, doc_lengths, index)
    # if cosine_scores[2] > cosine_scores[1] == cosine_scores[3] and isclose(cosine_scores[2], 0.017, abs_tol=1e-3):
    #     print("cosine_scores OK")
    # else:
    #     print("cosine_scores")


if __name__ == "__main__":
    main()
