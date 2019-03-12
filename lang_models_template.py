import glob
from bs4 import BeautifulSoup
import pickle
import re
import os
from collections import Counter


def extract_categories(path):
    """
    Parses .sgm files in path folder wrt categories each document belongs to.
    Returns a list of documents for each category. One document usually belongs to several categories.
    Categories are contained in special tags (<TOPICS>, <PLACES>, etc.),
    see cat_descriptions_120396.txt file for details
    :param path: original data path
    :return: dict, category:[doc_id1, doc_id2, ...]
    """
    # TODO write your code here


def lm_rank_documents(query, doc_ids, doc_lengths, high_low_index, smoothing, param):
    """
    Scores each document in doc_ids using this document's language model.
    Applies smoothing. Looks up term frequencies in high_low_index
    :param query: dict, term:count
    :param doc_ids: set of document ids to score
    :param doc_lengths: dictionary doc_id:length
    :param high_low_index: high-low index you built last lab
    :param smoothing: which smoothing to apply, either 'additive' or 'jelinek-mercer'
    :param param: alpha for additive / lambda for jelinek-mercer
    :return: dictionary of scores, doc_id:score
    """
    # TODO write your code here


def lm_define_categories(query, cat2docs, doc_lengths, high_low_index, smoothing, param):
    """
    Same as lm_rank_documents, but here instead of documents we score all categories
    to find out which of them the user is probably interested in. So, instead of building
    a language model for each document, we build a language model for each category -
    (category comprises all documents belonging to it)
    :param query: dict, term:count
    :param cat2docs: dict, category:[doc_id1, doc_id2, ...]
    :param doc_lengths: dictionary doc_id:length
    :param high_low_index: high-low index you built last lab
    :param smoothing: which smoothing to apply, either 'additive' or 'jelinek-mercer'
    :param param: alpha for additive / lambda for jelinek-mercer
    :return: dictionary of scores, category:score
    """
    # TODO write your code here


def extract_categories_descriptions(path):
    """
    Extracts full names for categories, draft version (inaccurate).
    You can use if as a draft for incorporating LM-based scoring to your engine
    :param path: original data path
    :return: dict, category:description
    """
    category2descr = {}
    pattern = r'\((.*?)\)'
    with open(path + 'cat-descriptions_120396.txt', 'r') as f:
        for line in f:
            if re.search(pattern, line) and not (line.startswith('*') or line.startswith('@')):
                category = re.search(pattern, line).group(1)
                if len(category.split()) == 1:
                    category2descr[category.lower()] = line.split('(')[0].strip()
    return category2descr


