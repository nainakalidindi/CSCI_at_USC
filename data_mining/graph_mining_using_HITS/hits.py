from pyspark import SparkContext, SparkConf
import time
import sys
import math
from io import StringIO

in_file = sys.argv[1]
nodes   = int(sys.argv[2])
num_of_iter = int(sys.argv[3])

conf = SparkConf().setAppName("hw5_spark")
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
lines = sc.textFile(in_file)
lines_mapped = lines.map(lambda x: (int(x.split('\t')[0]),int(x.split('\t')[1])))

b = sc.parallelize([x for x in range(1,nodes+1)])
authorities_list = b.map(lambda x: (x, 1.0))
hub_list = authorities_list

out_links = lines_mapped
temp_str = ""
def calculate_authorities(hub_list):
    authorities_list = out_links.join(hub_list) \
            .map(lambda x: (x[1][0], x[1][1])) \
            .reduceByKey(lambda x, y: x + y)
    return authorities_list


def calculate_hub(authorities_list):
    hub_list = out_links.map(lambda x: (x[1], x[0])) \
            .join(authorities_list) \
            .map(lambda x: (x[1][0], x[1][1])) \
            .reduceByKey(lambda x, y: x + y)
    return hub_list


def normalize(rdd):
    temp = list(rdd.values().take(100000))
    norm = max(temp)
    updated = rdd.map(lambda x: (x[0], x[1] / norm))
    return updated

for i in range(num_of_iter):
    start = time.time()
    print("Iteration:  "+str(i + 1))
    authorities_list = calculate_authorities(hub_list)
    hub_list = calculate_hub(authorities_list)
    authorities_list = normalize(authorities_list)
    hub_list = normalize(hub_list)
    print("\tAuthorities: ")
    for i in list(authorities_list.take(1000000)):
        print("\t \t"+str(i[0])+"  "+"%.2f" % i[1])
    print("\thub_list: ")
    for i in list(hub_list.take(1000000)):
        print("\t \t"+str(i[0])+"  "+"%.2f" % i[1])
