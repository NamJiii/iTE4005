import sys
import math

cluster_list = []

def neighbor_check(raw_data, my_id, eps):
    neighbors = []
    me = raw_data[my_id][1:]
    
    for neighbor_id in range(len(raw_data)):
        other = raw_data[neighbor_id][1:]
        if (math.sqrt(math.pow(float(me[0])-float(other[0]),2)+math.pow(float(me[1])-float(other[1]),2))<eps):
            neighbors.append(neighbor_id)
    
    return neighbors

def spread_cluster(raw_data, neighbors, eps, cluster_label, minPts):
    global cluster_list
    while len(neighbors) > 0:
        neighbor_id = neighbors[0]
        child_list = neighbor_check(raw_data, neighbor_id, eps)
            
        if len(child_list) >= minPts: 
                    
            for i in range(len(child_list)): 
                index = child_list[i]
                if cluster_list[index] == None :
                        
                    neighbors.append(index) 
                    cluster_list[index] = cluster_label 
            
        neighbors = neighbors[1:] 
            
def labeling(raw_data, my_id, cluster_label, eps, minPts): 
    global cluster_list
    
    neighbors = neighbor_check(raw_data, my_id, eps)

    if len(neighbors) >= minPts: 
        cluster_list[my_id] = cluster_label 
        
        for neighbor_id in neighbors: 
            cluster_list[neighbor_id] = cluster_label
        spread_cluster(raw_data, neighbors, eps, cluster_label, minPts)
        return True
    
    else:
        cluster_list[my_id] = -1
        return False

if __name__ == '__main__':
    raw_data = []
    
    with open(sys.argv[1], 'r') as f:
        input_ = f.read().split('\n') 
        for data in input_:
            data = data.split('\t')
            raw_data.append(data)
   
    raw_data = raw_data[:-1]

    cluster_number = int(sys.argv[2])
    eps = int(sys.argv[3])
    minPts = int(sys.argv[4])

    cluster_label = 0
    cluster_list = [None] * len(raw_data)

    for my_id in range(len(raw_data)-1,0,-1):
        if cluster_list[my_id] == None:
            if labeling(raw_data, my_id, cluster_label, eps, minPts):
                print("Cluster %s: generated" % cluster_label)
                cluster_label = cluster_label + 1

    input_name = sys.argv[1].replace('.txt', '')
    
    for label in range(len(set(cluster_list))-1):
        file_name = input_name + '_cluster_' + str(label) + '.txt'
        
        ID_list = [i for i, j in enumerate(cluster_list) if j == label]
        
        temp = ''
        for id in ID_list:
            temp += str(id) + '\n'
        with open(file_name, 'w') as f:
            f.write(temp)
