import sys
filename = sys.argv[-1]

rdd_1 = sc.textFile(sys.argv[1])
rdd_2 = sc.textFile(sys.argv[2])


#rdd_1 = sc.textFile('/home/nilkanth/eclipse-workspace/city-sample.txt')
#rdd_2 = sc.textFile('/home/nilkanth/eclipse-workspace/couuntry.txt')



def Func1(lines):
...    lines = lines.split('\t')
...    if (int(lines[4]) > 1000000):
...       lines_r = (lines[2] , 1) 
...       return lines_r

rdd_1_1 = rdd_1.map(Func1).filter(lambda x: x!= None).groupByKey().mapValues(list).filter(lambda x : len(x[1]) >=3)
rdd_2_2 = rdd_2.map(lambda x: (x.split('\t')[0], x.split('\t')[1]))

df1 = spark.createDataFrame(rdd_1_1, schema=['a', 'b'])
df2 = spark.createDataFrame(rdd_2_2, schema=['a', 'c'])
rdd_join = df1.join(df2, on='a')
rdd_final = rdd_join.rdd
rdd_out = rdd_final.map(lambda x: (x[2], len(x[1]) )).collect()


with open(sys.argv[2], 'w') as f:
    for item in rdd_out:
        f.write("%s\n" % item)

