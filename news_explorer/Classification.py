from __future__ import print_function

from time import time
import sys
import os
import numpy as np
import scipy.sparse as sp
import pylab as pl

from sklearn.datasets import load_mlcomp
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB

from news_explorer.models import Article
from news_explorer.models import ArticleByCategory

def classifyDocs():
    # Load the training set
    print("Loading newsgroups training set... ")
    news_train = load_files('news_explorer/train')
    print("%d documents" % len(news_train.filenames))
    print("%d categories" % len(news_train.target_names))
    print()

    print("Extracting features from the dataset using a sparse vectorizer")
    vectorizer = TfidfVectorizer(encoding='latin1')
    X_train = vectorizer.fit_transform((open(f).read()
                                        for f in news_train.filenames))
    print("n_samples: %d, n_features: %d" % X_train.shape)
    print()
    assert sp.issparse(X_train)
    y_train = news_train.target

    print("Loading newsgroups test set... ")
    A = Article.objects.values('id', 'headline', 'content')

    ids = []
    content = []
    for a in A:
        ids.append(a['id'])
        content.append(a['content'])

    X_test = vectorizer.transform(content)

    print("n_samples: %d, n_features: %d" % X_test.shape)
    print()

    ###############################################################################
    # Benchmark classifiers
    def benchmark(clf_class, params, name):
        t0 = time()
        clf = clf_class(**params).fit(X_train, y_train)

        print("Predicting the outcomes of the testing set")
        t0 = time()
        pred = clf.predict(X_test)

        for i in range(len(pred)):
            abc = ArticleByCategory(article_id = ids[i], category = news_train.target_names[pred[i]])
            abc.save()

    parameters = {
        'loss': 'hinge',
        'penalty': 'l2',
        'n_iter': 50,
        'alpha': 0.00001,
        'fit_intercept': True,
    }

    benchmark(SGDClassifier, parameters, 'SGD')

    pl.show()
