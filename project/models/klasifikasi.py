import pandas as pd
import numpy as np
import pickle, os, time
# from sklearn.model_selection import train_test_split
from .preprocessing import progreSignal
from .knn import KNN
from .mknn import MKNN

from sklearn.metrics import accuracy_score, confusion_matrix

def progreKlasi():
    testSignal, testLabel = progreSignal()
    X = pd.DataFrame(testSignal).dropna()
    y = pd.DataFrame(testLabel).dropna()

    reskNN = progrekNN(X, y)
    resMkNN = progreMkNN(X, y)

    return reskNN, resMkNN

def progrekNN(X, y):
    filename = os.path.join('./project/models/modules/', 'modelkNN.pkl')
    with open(filename, 'rb') as f:
        loadkNN = pickle.load(f)    
    start_time = time.time()
    predkNN = loadkNN.predict(X)
    kNN_time = time.time() - start_time
    kNN_time = round(kNN_time, 2)

    res, acc, preci, recall, fscore = conf_matrix(y, predkNN)

    return res, acc, preci, recall, fscore, kNN_time

def progreMkNN(X, y):
    filename = os.path.join('./project/models/modules/', 'modelMkNN.pkl')
    with open(filename, 'rb') as f:
        loadMkNN = pickle.load(f)    
    start_time = time.time()
    predMkNN = loadMkNN.predict(X)
    MkNN_time = time.time() - start_time
    MkNN_time = round(MkNN_time, 2)

    res, acc, preci, recall, fscore = conf_matrix(y, predMkNN)

    return res, acc, preci, recall, fscore, MkNN_time

def conf_matrix(y, pred):
    cfm = confusion_matrix(y[:len(pred)], pred, labels=["Healthy control", "Myocardial infarction"])
    trueNegative   = cfm[0][0]
    falsePositive = cfm[0][1]
    falseNegative = cfm[1][0]
    truePositive   = cfm[1][1]

    accH = round((falseNegative + falsePositive) / len(pred) * 100, 2)
    accM = round((trueNegative + truePositive) / len(pred) * 100, 2)

    if accH > accM:
        res = "Healthy control"
        acc = accH
        preci = round(trueNegative / (trueNegative + falseNegative) * 100, 2)
        recall = round(trueNegative / (trueNegative + falsePositive) * 100, 2)
        fscore = round(2 * (preci * recall) / (preci + recall), 2)
    else:
        res = "Myocardial infarction"
        acc = accM
        preci = round(truePositive / (truePositive + falsePositive) * 100, 2)
        recall = round(truePositive / (truePositive + falseNegative) * 100, 2)
        fscore = round(2 * (preci * recall) / (preci + recall), 2)

    return res, acc, preci, recall, fscore


