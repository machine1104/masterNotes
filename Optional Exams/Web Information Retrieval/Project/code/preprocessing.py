import json
import re
from collections import Counter, defaultdict
from os import path

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from tqdm import tqdm


def sample_file(input_file, output_file, rate):
    with open(input_file, encoding="utf8") as i:
        with open(output_file, "w", encoding="utf8") as o:
            for line in i.readlines():
                if np.random.rand() < rate:
                    o.write(line)


def parse_ttl(input_file):
    with open(input_file, encoding="utf8") as f:
        for line in f.readlines():
            tokens = line.split()
            yield (tokens[0][1:-1], tokens[2][1:-1])

"""
Removing stopwords and stemming with PorterStemmer.
"""

def preprocess(line):
    res = []
    ps = PorterStemmer()
    stop_words = stopwords.words("english")
    line = re.sub("[^a-zA-Z0-9]+", " ", line)
    for t in word_tokenize(line, language="english"):
        for t in map(str.lower, re.findall("[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))|[a-z]+|[A-z]+|[0-9]+", t)):
            if len(t) > 1 and t not in stop_words:
                res.append(ps.stem(t))
    return " ".join(res)


if __name__ == "__main__":

    # DATASETS (the archives have to be extracted in ./datasets/ directory)
    # ARTICLES  ==> http://downloads.dbpedia.org/2016-10/core-i18n/en/article_categories_en.ttl.bz2
    # REDIRECTS ==> http://downloads.dbpedia.org/2016-10/core-i18n/en/redirects_en.ttl.bz2

    """
    Retrieving articles and redirections from ttl datasets.
    """

    title_prefix = "http://dbpedia.org/resource/"
    category_prefix = "http://dbpedia.org/resource/Category:"

    articles_file = path.join("datasets", "article_categories_en.ttl")
    sampled_articles_file = path.join("datasets", "article_categories_en_sampled.ttl")
    redirects_file = path.join("datasets", "redirects_en.ttl")
    sampled_redirects_file = path.join("datasets", "redirects_en_sampled.ttl")

    sample_file(articles_file, sampled_articles_file, 0.05)
    sample_file(redirects_file, sampled_redirects_file, 0.15)

    ######################################################################################################################################################
    
    """
    Retrieving categories list and saving it to file. Only categories with related articles >5 AND <5000.
    """

    categories = Counter()
    for _, category in tqdm(parse_ttl(sampled_articles_file), desc="categories"):
        category = category[len(category_prefix):]
        if str(category).endswith("_stubs"):
            categories.update([category[:-6]])
        else:
            categories.update([category])
    categories = {k: v for k, v in categories.items() if (v >= 5 and v <= 5000)}
    json.dump(categories, open(path.join("vocabs", "categories.json"), "w", encoding="utf8"), ensure_ascii=False)
    
    ######################################################################################################################################################

    """
    Building a dictionary (key:value) where key = article title (full) and value = list of its related category
    and saving it to file.
    """

    article2category = defaultdict(list)
    for title, category in tqdm(parse_ttl(sampled_articles_file), desc="article2category"):
        category = category[len(category_prefix):]
        title = title[len(title_prefix):]
        if category in categories and category not in article2category[title]:
            article2category[title].append(category)
    json.dump(article2category, open(path.join("vocabs", "article2category.json"), "w", encoding="utf8"), ensure_ascii=False)
    
    ######################################################################################################################################################

    """
    Building a dictionary (key:value) where key = "clean" article title (no stopwords + stemming) and value = list of its related full
    title and saving it to file.
    """

    stemmed_title2article = defaultdict(list)
    for title in tqdm(article2category, desc="stemmed_title2article (articles)"):
        stemmed_title = preprocess(title)
        if len(stemmed_title) > 1 and title not in stemmed_title2article[stemmed_title]:
            stemmed_title2article[stemmed_title].append(title)
    for redirect, title in tqdm(parse_ttl(sampled_redirects_file), desc="stemmed_title2article (redirects)"):
        redirect = preprocess(redirect[len(title_prefix):])
        title = title[len(title_prefix):]
        if len(redirect) > 1 and title in article2category and title not in stemmed_title2article[redirect]:
            stemmed_title2article[redirect].append(title)
    json.dump(stemmed_title2article, open(path.join("vocabs", "stemmed_title2article.json"), "w", encoding="utf8"), ensure_ascii=False)
    
    ######################################################################################################################################################

    """
    Building a dictionary (key:value) where key = stem and value = list of its related stemmed
    title and saving it to file.
    """

    stem2stemmed_title = defaultdict(list)
    for stemmed_title in tqdm(stemmed_title2article, desc="stem2stemmed_title"):
        for stem in stemmed_title.split():
            if stemmed_title not in stem2stemmed_title[stem]:
                stem2stemmed_title[stem].append(stemmed_title)
    json.dump(stem2stemmed_title, open(path.join("vocabs", "stem2stemmed_title.json"), "w", encoding="utf8"), ensure_ascii=False)
    
    ######################################################################################################################################################

    """
    Building a dictionary (key:value) where key = category and value = list of all stems in its related articles
    and an other one where key = stem and value = total of category in which it is and saving both to files.
    """

    stem_category_frequency = defaultdict(list)
    category_vocab = defaultdict(list)
    for stemmed_title, articles in tqdm(stemmed_title2article.items(), desc="stem_category_frequency/category_vocab"):
        for stem in stemmed_title.split():
            for article in articles:
                for category in article2category[article]:
                    if stem not in category_vocab[category]:
                        category_vocab[category].append(stem)
                    if category not in stem_category_frequency[stem]:
                        stem_category_frequency[stem].append(category)
    stem_category_frequency = {k: len(v) for k, v in stem_category_frequency.items()}
    json.dump(stem_category_frequency, open(path.join("vocabs", "stem_category_frequency.json"), "w", encoding="utf8"), ensure_ascii=False)
    json.dump(category_vocab, open(path.join("vocabs", "category_vocab.json"), "w", encoding="utf8"), ensure_ascii=False)
    
    ######################################################################################################################################################
