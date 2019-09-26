
# coding: utf-8

# In[1]:


import sys
import itertools
from itertools import groupby
import random
import string
from operator import itemgetter
from functools import reduce
import collections
# a = [(random.randint(1, 3), random.choice('abcdef')) for _ in range(20)]


# In[2]:


text_file = open(sys.argv[1], "r")
lines = text_file.readlines()
text_file.close()


# In[3]:


initial_list = [[i.split(',')[1][0] , i.split(',')[0]]  for i in lines]
sorted_initial_list = sorted(initial_list, key=lambda x: x[0])


# In[4]:


key_list = []
value_list = []
for key, group in groupby(sorted_initial_list, key=lambda x: x[0]):
    key_list.append(key)
    value_list.append(list(group))
    
value_list_2 = [[j[1] for j in i] for i in value_list]
value_list_3 = [sorted(list(dict.fromkeys(i))) for i in value_list_2]

bucket_data = list(zip(key_list, value_list_3))


# In[5]:


a1 = [[j for j in i[1]] for i in bucket_data]
b1 = list(itertools.chain.from_iterable(a1))


# In[6]:


counter = collections.Counter(b1)
count_table = list(zip(counter.keys(), counter.values()))
#count_table


# In[7]:


threshold = int(sys.argv[3])
size_of_itemset = int(sys.argv[2])

candidate_list = [i[0] for i in count_table if i[1]>= threshold] 
candidate_list


#set_list = []


# In[8]:


def pair_gen(candidate_list, current_size):
    #print(candidate_list)
    #print(current_size)
    #set_list_1 = list(itertools.combinations(candidate_list, current_size-1))
    set_list_1 = sorted(list(reduce(lambda i, j: set(i) | set(j), 
                                    sorted([list(itertools.combinations(sorted(set(j[0]).union(j[1])), current_size))
                                    for j in [i for i in (list(itertools.combinations(candidate_list, 2)))]]) )))
    #print(set_list)
    set_list = set_list_1
    return set_list



def check_candidate(set_list):    
    #print(set_list)
    new_candidate_list = []
    for i in set_list:
        temp_baskets = []
        for j in bucket_data:
            if (set(i).issubset(j[1])):
                #print(i , j[0])
                temp_baskets.append(j[0])            
        new_candidate_list.append([i,temp_baskets]) 
        #print(new_candidate_list)

    true_candidate_list_1 = [i for i in new_candidate_list if len(i[1]) >= threshold]
    true_candidate_list = [i[0] for i in true_candidate_list_1]
    true_candidate_names = [i[1] for i in true_candidate_list_1]
    
    #print(true_candidate_list)
    candidate_list = true_candidate_list  
    candidate_names= true_candidate_names
    
    return candidate_list, candidate_names


# In[9]:


if (size_of_itemset >1):
    for i in range(2,size_of_itemset+1):
        #print(i)
        set_list = pair_gen(candidate_list, i)
        #print("set_list =", set_list)
        candidate_list, candidate_names = check_candidate(set_list)
        #print("candidate_LIST = ", candidate_list)


if (size_of_itemset >1):
    for i in range(2,size_of_itemset+1):
        #print(i)
        set_list = pair_gen(candidate_list, i)
        #print("set_list =", set_list)
        candidate_list, candidate_names = check_candidate(set_list)
        #print("candidate_LIST = ", candidate_list)

for i in range(len(candidate_names)):
    if (len(candidate_names[i]) > threshold):
        candidate_names[i] = list(itertools.combinations(candidate_names[i], threshold))
    
        
        
for i in range(len(candidate_names)): 
    if (len(candidate_names[i][0])>1):
        for j in range(len(candidate_names[i])):
            print("{"+str(candidate_list[i])[1:-1].replace("'","")+"}","{"+str(candidate_names[i][j])[1:-1].replace("'","")+"}")
    else:
        print("{"+str(candidate_list[i])[1:-1].replace("'","")+"}","{"+str(candidate_names[i])[1:-1].replace("'","")+"}")


