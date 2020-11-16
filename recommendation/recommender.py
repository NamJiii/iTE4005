import math
import sys

def pearson_eq(related_item,leng,new_user,train_user):
    rate_sum1,rate_sum2 = 0,0
    rate_sq1,rate_sq2 = 0,0
    multiplied=0
    for item in related_item:
        tmp1,tmp2=trains[new_user][item],trains[new_user][item]
        rate_sum1 += tmp1
        rate_sum2 += tmp2
        rate_sq1 += tmp1**2
        rate_sq2 += tmp2**2
        multiplied += tmp1 * tmp2 

    if ((rate_sq1 - (rate_sum1 * rate_sum1) / leng)==0 or (rate_sq2 - (rate_sum2 * rate_sum2) / leng)==0):
        return 0
    else:
        return (multiplied - (rate_sum1 * rate_sum2 / leng)) / math.sqrt((rate_sq1 - (rate_sum1 * rate_sum1) / leng)* (rate_sq2 - (rate_sum2 * rate_sum2) / leng))
    
def correlation(trains, new_user, train_user):
    related_item = dict()
    for item in trains[new_user]:
        if item in trains[train_user]: 
            related_item[item] = 1
    leng = len(related_item)
    if leng != 0: 
        return pearson_eq(related_item,leng,new_user,train_user)
    else:
        return 0

def find_neighbor(trains, new_user):
    pearson_item = dict()
    recommend_rate = dict()

    for train_user in trains:
        if train_user != new_user:
            correlatance = correlation(trains, new_user, train_user)
            if correlatance > 0:
                for item in trains[train_user]:
                    if item not in trains[new_user] or trains[new_user][item] == 0:
                        pearson_item.setdefault(item, 0)
                        pearson_item[item] += correlatance
                        recommend_rate.setdefault(item, 0)
                        recommend_rate[item] += trains[train_user][item] * correlatance
    neighbor = [(total / pearson_item[item], item) for item, total in recommend_rate.items()]

    return neighbor

def cf_algorithm(trains, tests):
    total_user = list()
    new = set()
    get_rate = list()
    
    for test_ in tests:
        if test_[0] not in new:
            neighbor = find_neighbor(trains, test_[0])
        new.add(test_[0])

        for item in neighbor:
            if item[1] == test_[1]:
                get_rate.append(item[0])

        if len(get_rate) == 0: 
            get_rate = [4]
        
        test_ = [test_[0], test_[1], get_rate[0]]
        total_user.append(test_)

    return total_user

if __name__ == "__main__":
    trains = {}
    tests = []

    with open(sys.argv[1], 'r') as f:
        input_data = f.read().split('\n')
        input_data = input_data[:-1]

        for test_ in input_data:
            data = test_.split('\t')
            user, item, rating, ts = data[0], data[1], data[2], data[3]
            trains.setdefault(user, {})
            trains[user][item] = int(rating)

    with open(sys.argv[2], 'r') as f:
        input_data = f.read().split('\n')
        input_data = input_data[:-1]

        for test_ in input_data:
            data = test_.split('\t')
            user, item, rating, ts = data[0], data[1], data[2], data[3]
            tests.append((user, item, rating, ts))
    
    recommended_set = cf_algorithm(trains, tests)
    output_name = sys.argv[1] + '_prediction.txt'
    with open(output_name, 'w') as f:
        for i in range(len(recommended_set)):
            line = ''
            for j in range(len(recommended_set[0])):
                line += '%s\t' % (recommended_set[i][j])
            line = line[:-1]
            line += '\n'
            
            f.write(line)
