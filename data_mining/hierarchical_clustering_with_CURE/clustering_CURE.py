import heapq
import itertools
import sys
import os
import math

class CURE_Clustering:    
    def __init__(self, input_data, input_k):        
        self.file_name = input_data
        self.clusters = []
        
        self.gold_standard = {}
        self.k = input_k
        
        self.dataset = None
        
        self.dataset_size = 0
        self.dimension = 0
        self.heap = []                
    
    def ec_dist(self, point_1, point_2):
        size = len(point_1)
        result = 0.0
        for i in range(size):
            f1 = float(point_1[i])   # feature for data one
            f2 = float(point_2[i])   # feature for data two
            tmp = f1 - f2
            result += pow(tmp, 2)
        result = math.sqrt(result)
        return result

    def dist_pairs(self, dataset):
        result = []
        dataset_size = len(dataset)
        for i in range(dataset_size-1):    # ignore last i
            for j in range(i+1, dataset_size):     # ignore duplication
                dist = self.ec_dist(dataset[i]["line"], dataset[j]["line"])
                result.append( (dist, [dist, [[i], [j]]]) )

        return result
    
    def build_priority_queue(self, distance_list):
        heapq.heapify(distance_list)
        self.heap = distance_list
        return self.heap

    def initialize(self):
        self.dataset, self.clusters, self.gold_standard = self.load_data(self.file_name)
        self.dataset_size = len(self.dataset)

        self.dimension = len(self.dataset[0]["line"])
    
    
    
    
    def compute_cntr_two_clusters(self, current_clusters, data_points_index):
        size = len(data_points_index)
        dim = self.dimension
        cntr = [0.0]*dim
        for index in data_points_index:
            dim_data = current_clusters[str(index)]["center"]
            for i in range(dim):
                cntr[i] += float(dim_data[i])
        for i in range(dim):
            cntr[i] /= size
        return cntr
    

    def compute_cntr(self, dataset, data_points_index):
        size = len(data_points_index)
        dim = self.dimension
        cntr = [0.0]*dim
        for idx in data_points_index:
            dim_data = dataset[idx]["line"]
            for i in range(dim):
                cntr[i] += float(dim_data[i])
        for i in range(dim):
            cntr[i] /= size
        return cntr

    def cc_clust(self):
        dataset = self.dataset
        current_clusters = self.clusters
        old_clusters = []
        heap = cc.dist_pairs(dataset)
        heap = cc.build_priority_queue(heap)

        while len(current_clusters) > self.k:
            dist, min_item = heapq.heappop(heap)
            # pair_dist = min_item[0]
            pair_data = min_item[1]

            # judge if include old cluster
            if not self.valid_heap_node(min_item, old_clusters):
                continue

            new_cluster = {}
            new_cluster_elements = sum(pair_data, [])
            new_cluster_cendroid = self.compute_cntr(dataset, new_cluster_elements)
            new_cluster_elements.sort()
            new_cluster.setdefault("center", new_cluster_cendroid)
            new_cluster.setdefault("elements", new_cluster_elements)
            for pair_item in pair_data:
                old_clusters.append(pair_item)
                del current_clusters[str(pair_item)]
            self.add_heap_entry(heap, new_cluster, current_clusters)
            current_clusters[str(new_cluster_elements)] = new_cluster
        sorted(current_clusters)
        #current_clusters.sort()
        return current_clusters
            
    def valid_heap_node(self, heap_node, old_clusters):
        pair_dist = heap_node[0]
        pair_data = heap_node[1]
        for old_cluster in old_clusters:
            if old_cluster in pair_data:
                return False
        return True
            
    def add_heap_entry(self, heap, new_cluster, current_clusters):
        for ex_cluster in current_clusters.values():
            new_heap_entry = []
            dist = self.ec_dist(ex_cluster["center"], new_cluster["center"])
            new_heap_entry.append(dist)
            new_heap_entry.append([new_cluster["elements"], ex_cluster["elements"]])
            heapq.heappush(heap, (dist, new_heap_entry))

    def evaluate(self, current_clusters):
        gold_standard = self.gold_standard
        current_clustes_pairs = []

        for (current_cluster_key, current_cluster_value) in current_clusters.items():
            tmp = list(itertools.combinations(current_cluster_value["elements"], 2))
            current_clustes_pairs.extend(tmp)
        tp_fp = len(current_clustes_pairs)

        gold_standard_pairs = []
        for (gold_standard_key, gold_standard_value) in gold_standard.items():
            tmp = list(itertools.combinations(gold_standard_value, 2))
            gold_standard_pairs.extend(tmp)
        tp_fn = len(gold_standard_pairs)

        tp = 0.0
        for ccp in current_clustes_pairs:
            if ccp in gold_standard_pairs:
                tp += 1

        if tp_fp == 0:
            precision = 0.0
        else:
            precision = tp/tp_fp
        if tp_fn == 0:
            precision = 0.0
        else:
            recall = tp/tp_fn

        return precision, recall

    def load_data(self, file_name):
        input_file = open(file_name, 'r')
        dataset = []
        clusters = {}
        gold_standard = {}
        id = 0
        for line in input_file:
            line = line.strip('\n')
            row = str(line)
            row = row.split(",")
            iris_class = row[-1]

            data = {}
            data.setdefault("id", id)   # duplicate
            data.setdefault("line", row[:-1])
            data.setdefault("class", row[-1])
            dataset.append(data)

            clusters_key = str([id])
            clusters.setdefault(clusters_key, {})
            clusters[clusters_key].setdefault("center", row[:-1])
            clusters[clusters_key].setdefault("elements", [id])

            gold_standard.setdefault(iris_class, [])
            gold_standard[iris_class].append(id)

            id += 1
        return dataset, clusters, gold_standard



    def display(self, current_clusters, precision, recall):

        clusters = current_clusters.values()
        for cluster in clusters:
            cluster["elements"].sort()
            print('Cluster: {}'.format(cluster["elements"]))
        print("Precision = " + str(precision))
        print("Recall = " + str(recall))

input_k = int(sys.argv[1])
input_data = sys.argv[2]
full_data = sys.argv[2]
rep_set_size = int(sys.argv[4])
prec_move = float(sys.argv[5])
    


cc = CURE_Clustering(input_data, input_k)
cc.initialize()
current_clusters = cc.cc_clust()
precision, recall = cc.evaluate(current_clusters)
cc.display(current_clusters, precision, recall)

