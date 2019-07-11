import json
from os import path

import matplotlib.pyplot as plt
import numpy as np
import requests
from tqdm import tqdm

from classification import predict_categories


def plot(title, x_lab, y_lab, x, y, x_tick=None, y_tick=None):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    if x_tick is not None:
        plt.xticks(x_tick)
    if y_tick is not None:
        plt.yticks(y_tick)
    plt.savefig(path.join("output", title+".png"))
    plt.show()


if __name__ == "__main__":

    min_n = 1
    max_n = 10
    num_docs = 100

    categories = json.load(open(path.join("vocabs", "categories.json"), encoding="utf8"))
    article2category = json.load(open(path.join("vocabs", "article2category.json"), encoding="utf8"))
    stemmed_title2article = json.load(open(path.join("vocabs", "stemmed_title2article.json"), encoding="utf8"))
    stem2stemmed_title = json.load(open(path.join("vocabs", "stem2stemmed_title.json"), encoding="utf8"))
    category_vocab = json.load(open(path.join("vocabs", "category_vocab.json"), encoding="utf8"))
    stem_category_frequency = json.load(open(path.join("vocabs", "stem_category_frequency.json"), encoding="utf8"))

    test_dataset = []
    test_titles = [k for k, v in article2category.items() if len(v) >= min_n]
    test_titles = np.random.choice(test_titles, num_docs)
    for title in tqdm(test_titles, desc="test_titles"):
        params = {"action": "query", "format": "json", "titles": title, "prop": "extracts", "explaintext": True, "exlimit": 1}
        response = requests.get("https://en.wikipedia.org/w/api.php", params=params).json()
        try:
            test_dataset.append((title, list(response["query"]["pages"].values())[0]["extract"]))
        except KeyError:
            pass
    print()

    precision = []
    recall = []
    predictions = []
    for title, document in test_dataset:
        p = []
        r = []
        pred = predict_categories(document, categories, article2category, stemmed_title2article,
                                  stem2stemmed_title, category_vocab, stem_category_frequency)[:max_n]
        true = article2category[title]
        for i in range(1, max_n+1):
            num = len([c for c in pred[:i] if c in true])
            p.append(num/i)
            r.append(num/len(true))
        precision.append(p)
        recall.append(r)
        predictions.append((title, true, pred))
        print()

    avg_precision = np.array(precision).mean(axis=0)
    plot("Precision@K", "K", "Precision", range(1, max_n+1), avg_precision, x_tick=range(1, max_n+1))
    avg_recall = np.array(recall).mean(axis=0)
    plot("Recall@K", "K", "Recall", range(1, max_n+1), avg_recall, x_tick=range(1, max_n+1))

    with open(path.join("output", "predictions.txt"), "w", encoding="utf8") as f:
        for title, true, pred in predictions:
            f.write(title + "\t" + str(true) + "\t" + str(pred) + "\n")
