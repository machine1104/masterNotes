import json
from collections import Counter, defaultdict
from math import log
from os import path

from tqdm import tqdm

from preprocessing import preprocess


def supports(word, stemmed_title, corpus_vocab):
    tokens = stemmed_title.split()
    if word in tokens:
        tokens.remove(word)
        count = 0
        for t in tokens:
            if t not in corpus_vocab:
                count += 1
                if count == 2:
                    return False
        return True
    else:
        return False


def predict_categories(document, categories, article2category, stemmed_title2article, stem2stemmed_title, category_vocab, stem_category_frequency):

    ######################################################################################################################################################
    preprocessed_doc = [t for t in preprocess(document).split() if t in stem2stemmed_title]
    doc_vocab = Counter()
    doc_vocab.update(preprocessed_doc)
    ######################################################################################################################################################

    ######################################################################################################################################################
    doc_score = {}
    for word, frequency in tqdm(doc_vocab.items(), desc="doc_score"):
        doc_score[word] = frequency * log(len(categories)/stem_category_frequency[word])
    ######################################################################################################################################################

    ######################################################################################################################################################
    article_score = {}
    category_supporting_word = defaultdict(set)
    for stemmed_title, articles in tqdm(stemmed_title2article.items(), desc="article_score"):
        rt = 0
        found = 0
        at = len(articles)
        lt = len(stemmed_title.split())
        st = len([s for s in stemmed_title.split() if s in doc_score])
        for word, rw in doc_score.items():
            if supports(word, stemmed_title, doc_score.keys()):
                for article in articles:
                    for category in article2category[article]:
                        category_supporting_word[category].update([word])
                found = 1
                tw = len(stem2stemmed_title[word])
                rt += rw*(1/tw)*(1/at)*(st/lt)
        if found:
            for article in articles:
                if article not in article_score or article_score[article] < rt:
                    article_score[article] = rt
    ######################################################################################################################################################

    ######################################################################################################################################################
    category_score = {}
    for category, stems in tqdm(category_vocab.items(), desc="category_score"):
        vc = len(category_supporting_word[category])
        dc = len(stems)
        tot_ra = 0
        for article, ra in article_score.items():
            if category in article2category[article]:
                tot_ra += ra
        category_score[category] = (vc/dc)*tot_ra
    ######################################################################################################################################################

    ######################################################################################################################################################
    decay_value = {k: 1 for k, v in doc_vocab.items()}
    sorted_category_score = sorted(category_score.items(), key=lambda x: x[1], reverse=True)
    for category, score in tqdm(sorted_category_score, desc="improved_category_score"):
        num = sum([decay_value[stem] for stem in category_supporting_word[category]])
        den = len(category_supporting_word[category])
        if den != 0:
            category_score[category] = score*(num/den)
        for sw in category_supporting_word[category]:
            decay_value[sw] /= 2
    ######################################################################################################################################################

    return list(map(lambda x: x[0], sorted(category_score.items(), key=lambda x: x[1], reverse=True)))
