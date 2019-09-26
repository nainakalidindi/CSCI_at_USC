import os, sys
from pyspark import SparkContext
from operator import add
import itertools
import time
import copy
import math
import csv


def append(a, b):
    a.append(b)
    return a

def calcJS(m1,m2):
    set_a = d1[m1]
    set_b = d1[m2]
    overlap = len(set_a & set_b)
    total = len(set_a) + len(set_b) - overlap
    return float(overlap)/float(total)

def makeSigMat(inputline):
    result_mat = list()
    for everymovie in inputline:
        res,band0,band1,band2,band3 = list(),list(),list(),list(),list()
        res.append(everymovie[0])
        movies_line = map(lambda m: int(m), everymovie[1:])
        if (len(list(movies_line))>0):
            for i in range(20):
                movies_line = map(lambda m: int(m), everymovie[1:])
                if i>=0 and i<=4:
                    band0.append(min(map(lambda m:(5*m+13*i)%100,movies_line)))
                elif i>=5 and i<=9:
                    band1.append(min(map(lambda m:(5*m+13*i)%100,movies_line)))
                elif i>=10 and i<=14:
                    band2.append(min(map(lambda m:(5*m+13*i)%100,movies_line)))
                elif i>=15 and i<=19:
                    band3.append(min(map(lambda m:(5*m+13*i)%100,movies_line)))
                movies_line = map(lambda m: int(m), everymovie[1:])

        res.append(band0)
        res.append(band1)
        res.append(band2)
        res.append(band3)
        result_mat.append(res)
    return result_mat

sc = SparkContext()
data = sc.textFile(sys.argv[1],minPartitions=None)
data0 = data.map(lambda x: (x.split(',')))
data1 = data.map(lambda x: (x.split(',')[0], x.split(',')[1:]))
data1.take(1)
data_new = data.map(lambda x: (x.split(','))).mapPartitions(makeSigMat)
data_new.take(2)
data_new_1 = data_new.map(lambda x: (x[0], x[1:])).flatMapValues(lambda x:x)
#d1 = data_new_1.map(lambda x: (x[1],x[0])).groupByKey().mapValues(set).collectAsMap()

output = open(sys.argv[2], "w")
for i in range(1, len(result_mat)):
    str1 = result_mat[i]
    output.write(str1)


