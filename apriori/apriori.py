import sys
import itertools
from pprint import pprint

data = []
dataFile = ''
resultFile = ''
minSup = 0

def candToSet(sets_):
    candidate = []
    for data_ in sets_:
        candidate.append(set(data_))
    candidate.sort()
    return candidate

def decision(length, rawFreq, Cand):
    global data
    Freq = dict() 
    
    for sets in Cand: 
        cnt = 0
        for datas in list(itertools.combinations(sets, length - 1)):
            if length == 2:
                datas = list(datas)
            else:
                datas = set(datas)

            if not datas in rawFreq:
                break
            cnt = cnt + 1
        
        if cnt == length:
            Freq[tuple(sets)] = 0 
    
    for key in Freq.keys():
        for element in data:
            if set(key) <= set(element): 
                Freq[key] = Freq[key] + 1
    return {key: Freq[key] for key in Freq.keys() if Freq[key] >= minSup} 

def calculate(length, setFr):
    for sets, freq in setFr.items():
        len_ = length
        support = 100 * freq/len(data)
        
        while True:
            temp = list(itertools.combinations(sets, len_-1))
            for item in temp:
                cnt = 0
                for element in data:
                    if set(element) >= set(item):
                        cnt = cnt + 1
                confidence = 100 * freq / cnt

                with open(resultFile,'a') as f:
                    f.write(str(set(map(int, set(item)))) + '\t' + str(set(map(int, set(sets)-set(item)))) + '\t' + str('%.2f' % round(support, 2)) + '\t' + str('%.2f' % round(confidence, 2)) + '\n')
               
            len_ = len_ - 1
            if len_ < 2 : break

            
def apriori_():
    global data
    sets = dict()
    for element in data:
        for item in element:
            if not item in sets.keys(): 
                sets[item] = 1
            else:
                sets[item] = sets[item] + 1 
    freq = {key: sets[key] for key in sets.keys() if sets[key] >= minSup}
    Freq = ['',freq]
    
    length = 2
    rawFreq = list(Freq[length-1].keys())
    newSet = []
    newSet = rawFreq
    newT = []
    for element in rawFreq:
        newT.append(list([element,]))
    rawFreq = newT
    
    while True:        
        candidate = candToSet(list(itertools.combinations(newSet, length)))
        end_check(candidate)

        candidate = decision(length, rawFreq, candidate)
        end_check(candidate)
        
        calculate(length, candidate)

        if candidate == -1: 
            exit()

        Freq.append(candidate)
        length = length + 1
        rawFreq = list(Freq[length - 1].keys())
        newSet = []
        for sets in rawFreq: 
            for datas in sets:
                if not datas in newSet: 
                    newSet.append(datas)
        rawFreq = candToSet(rawFreq)
                    
def end_check(c):
    if len(c) == 0:
        exit()
        
if __name__ == '__main__':
    option = sys.argv 
    dataFile = option[2]
    resultFile = option[3]

    with open(dataFile,'r') as f:
        for sets in f:
            data.append(sets.strip().split('\t'))

    minSup = len(data)*float(option[1])/100
    apriori_()
