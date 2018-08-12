from collections import defaultdict
from avg_perceptron import tagdict, weights

def tag(tokens):
    context = ['-START-', '-START2-']
    prev,prev2 = context
    context += [token.lower() for token in tokens] + ['-END-', '-END2-']
    tagged_tokens = []
    for i, token in enumerate(tokens):
        tag = tagdict.get(token)
        if not tag:
            tag = predict(get_features(i + 2, token, context, prev, prev2))
        tagged_tokens.append((token, tag))
        prev2 = prev
        prev = tag
    return tagged_tokens

def get_features(i, word, context, prev, prev2):
    def add(name, *args):
        features[' '.join((name,) + tuple(args))] += 1
    features = defaultdict(int)
    add('bias')
    add('i suffix', word[-3:])
    add('i pref1', word[0])
    add('i-1 tag', prev)
    add('i-2 tag', prev2)
    add('i tag+i-2 tag', prev, prev2)
    add('i word', context[i])
    add('i-1 tag+i word', prev, context[i])
    add('i-1 word', context[i-1])
    add('i-1 suffix', context[i-1][-3:])
    add('i-2 word', context[i-2])
    add('i+1 word', context[i+1])
    add('i+1 suffix', context[i+1][-3:])
    add('i+2 word', context[i+2])
    return features

def predict(features):
    classes = {",","UH","NNPS","VBP","DT","RB","VBZ","WRB","SYM","LS","PRP","PDT","$","#","TO","RP","VB","VBG","WP","FW","''","NN","-LRB-","JJS","JJR","NNS","EX","JJ","PRP$",":","RBR","CC","-RRB-",".","VBN","RBS","NNP","VBD","IN","CD","``","WP$","POS","MD","WDT",}
    scores = defaultdict(float)
    for feat, value in features.items():
        if feat not in weights or value == 0:
            continue
        w = weights[feat]
        for label, weight in w.items():
            scores[label] += value * weight
    return max(classes, key=lambda label: (scores[label], label))

# print(tag(input().split()))