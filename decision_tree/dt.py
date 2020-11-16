import pandas as pd
import math
import sys

class Tree():
    def __init__(self, inputs,is_leaf=0):
        self.is_leaf = is_leaf
        self.inputs = inputs
        self.decision = self.inputs.iloc[:,-1].value_counts().idxmax()
        if (not is_leaf): self.growing()
    
    def growing(self):
        self.attribute = maxR(self.inputs)
        self.classify(self.inputs[self.attribute])

    def classify(self, data_):
        values= data_.unique()
        self.children = dict()

        for value in values:
            modif= self.inputs.loc[self.inputs[self.attribute] == value]
            if len(modif.iloc[:,-1].unique()) == 1 : self.children[value] = Tree(modif, is_leaf=1)
            elif len(modif.columns) == 3 : self.children[value] = Tree(modif, is_leaf=1)
            else:
                self.children[value] = Tree(modif.drop(self.attribute, 1))

    def search(self, series):
        if (self.is_leaf):
            return self.decision
        value = series[self.attribute]
        try:
            childs = self.children[value]
        except:
            return self.decision
        return childs.search(series)

def entropy(prob):
    return sum(-p * math.log(p, 2) for p in prob if p)

def probability(values):
    total_count = len(values)
    return [float(value)/float(total_count) for value in values]

def ratio(table):
    total = table.values.sum()
    return sum(entropy(probability(val)) * len(val) / total for val in table.values)


def maxR(inputs):
    candidates = dict()
    for column in inputs.columns[:-1]:
        candidate = inputs[column]
        table = pd.crosstab(candidate, inputs[inputs.columns[-1]])
        candidates[column] = ratio(table)
    return min(candidates.keys(), key=(lambda k: candidates[k]))


if __name__ == '__main__':
    df_train = list()
    with open(sys.argv[1], 'r') as f:
        input_data = f.read().split('\n') 
        for data in input_data:
            data = data.split('\t')
            df_train.append(data)
    
    df_train = pd.DataFrame(df_train)
    header = df_train.iloc[0]
    df_train = df_train[1:-1]
    df_train.columns = header

    df_test = list()
    with open(sys.argv[2], 'r') as f:
        input_data = f.read().split('\n') 
        for data in input_data:
            data = data.split('\t')
            df_test.append(data)
    
    df_test = pd.DataFrame(df_test)
    header = df_test.iloc[0]
    df_test = df_test[1:-1]
    df_test.columns = header

    tree = Tree(df_train)

    header = df_train.columns
    header = list(header)
    with open(sys.argv[3], 'w') as f:
        new_line = ''
        for word in header:
            new_line += word+'\t' 
        f.write(new_line[:-1] + '\n') 

    for _, row in df_test.iterrows():
        line = row.values
        result = tree.search(row)
        line = list(line)
        line.append(result)

        with open(sys.argv[3], 'a') as f:
            new_line = ''
            for word in line:
                new_line += word+'\t' 
            f.write(new_line[:-1] + '\n')
