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
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing

from news_explorer.models import Article
from news_explorer.models import ArticleByCategory

def classifyDocs():
    target_names = ['Natural Disasters', 'Politics', 'Terrorism']

    # Load the training set
    print("Loading newsgroups training set... ")
    news_content = 'news_explorer/train/Content'
    news_labels = 'news_explorer/train/Labels'
    X_train = (open(news_content + "/" + f).read() for f in os.listdir(news_content))
    y_crude = (open(news_labels + "/" + f).read() for f in os.listdir(news_labels))
    y_train = []

    print(X_train)

    for y in y_crude:
        temp = y.split(",")
        arr = []
        for t in temp:
            arr.append(target_names.index(t.strip()))
        y_train.append(arr)

    print(X_train)
    print(y_train)

    print("Loading newsgroups test set... ")
    A = Article.objects.values('id', 'headline', 'content')

    ids = []
    content = []
    for a in A:
        ids.append(a['id'])
        content.append(a['content'])

    X_test = content

    print(len(X_test))

    lb = preprocessing.LabelBinarizer()

    ###############################################################################
    # Benchmark classifiers
    def benchmark():
        classifier = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', OneVsRestClassifier(LinearSVC()))])
        classifier.fit(X_train, lb.fit_transform(y_train))
        predicted = classifier.predict(X_test)
        all_labels = lb.inverse_transform(predicted)

        print(len(all_labels))
        print(len(X_test))

        for i in range(len(all_labels)):
            for label in all_labels[i]:
                abc = ArticleByCategory(article_id = ids[i], category = target_names[label])
                abc.save()

    benchmark()

    pl.show()
