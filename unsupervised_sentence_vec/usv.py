from re import search
from os import remove
from shutil import move
from requests import get
from bs4 import BeautifulSoup

def _clean(txt):
    cleaned = ''
    for letter in txt:
        if 97 <= ord(letter.lower()) <= 122 or letter.isdigit():
            cleaned += letter
        elif letter not in "'´-":
            cleaned += " "
    return ' '.join(cleaned.split())

def _extractionRule(keyword, sentence):
    PAD = " "
    sentence = PAD + sentence.lower() + PAD
    pattern = r" (.*) (be|is|am|are|was|were|means) (.*) "
    objs = search(pattern,sentence)
    if objs is not None:
        phrases = objs.groups()
        if keyword == phrases[0]:
            return phrases[-1]
        elif keyword == phrases[-1]:
            return phrases[0]

def extract_definition(keyword,sentence):
    # returns the definition for the keyword extracted from the sentence
    return _extractionRule(keyword, sentence)

def define(keyword):
    # finds definitions for the keyword using internet
    documents = search_internet(keyword)
    definitions = set([keyword])
    for document in documents:
        if document is not None:
            print('\n\n' + document)
            for sentence in document.split('. '):
                d = extract_definition(keyword,sentence)
                if d is not None:
                    definitions.add(d)
    return definitions

def getIds(phrases,filename='known_phrases.txt'):
    # if known - remember its id
    #checks if phrases are in the memory file 
    with open(filename) as memory:
        phrase_ids = []
        phrase_id = 0
        try:
            while True:
                words,_ = memory.readline().strip().split(':')
                if len(phrases) == 0:
                    break
                if words in phrases:
                    phrase_ids.append(phrase_id)
                    phrases ^= set([words])
                phrase_id += 1
        except:
            pass
    #if unknown - add it to end with empty vector.  remember its id
    #append new phrases with empty vectors to end of file
    with open(filename,'a') as memory:
        for phrase in phrases:
            memory.write(phrase + ': {}\n'.format(phrase_id))
            phrase_ids.append(phrase_id)
            phrase_id += 1
    return phrase_ids


def updateVecs(ids,filename='known_phrases.txt'):
    #for all ids - update the vectors 
    # vector is updated by including all new ids into it
    with open('temp' + filename,'w') as new_memory:
        with open(filename) as memory:
            phrase_id = 0
            try:
                while True:
                    words,vector = memory.readline().strip().split(':')
                    if phrase_id in ids:
                        vector = {int(v) for v in vector.split(',')} | set(ids)
                        new_memory.write(words + ': ' + ','.join([str(v) for v in vector]) + '\n')
                    else:
                        new_memory.write(words + ':' + vector + '\n')
                    phrase_id += 1
            except:
                pass
    remove(filename)
    move('temp'+filename, filename)


def learn(learn_these):
    if len(learn_these) == 0:
        return
    seed = list(learn_these)[0]
    definitions = define(seed)
    print('\n\ndefinition of "{}" is {}\n\n'.format(seed,definitions))
    updateVecs(getIds(definitions))
    learn_these |= definitions 
    learn_these ^= set([seed])
    learn(learn_these)

def _compare_sets(set_v1, set_v2): #1.0 = 0% identical
    return len(set_v1 ^ set_v2) / (len(set_v1) + len(set_v2) + 1e-8)

def _synonyms(target_v,filename = 'known_phrases.txt',capacity = 5,threshold=1.):
    best = []
    with open(filename) as memory:
        try:
            while True:
                word,vector = memory.readline().strip().split(':')
                vector = {int(v) for v in vector.split(',')}
                    
                cost = _compare_sets(target_v,vector)
                if cost <= threshold:
                    if len(best) < capacity:
                        best.append((cost,word))
                        best = sorted(best)
                    else:
                        for i in range(capacity):
                            if cost < best[i][0]:
                                best = best[:i] + [(cost,word)] + best[i:]
                                best.pop()
                                break
        except:
            pass
    return [w for _,w in best]

def _find_vector(key, filename = 'known_phrases.txt'):
    with open(filename) as memory:
        try:
            while True:
                word,vector = memory.readline().strip().split(':')
                if word == key:
                    return {int(v) for v in vector.split(',')}
        except:
            pass

def _find_phrases(phrase_ids,filename='known_phrases.txt'):
    phrases = []
    with open(filename) as memory:
        phrase_id = 0
        try:
            while True:
                words,_ = memory.readline().strip().split(':')
                if phrase_id in phrase_ids:
                    phrases.append(words)
                phrase_id += 1
        except:
            pass
    return phrases

def exact_meaning(word,filename='known_phrases.txt'):
    return _find_phrases(_find_vector(word))

def similar_meaning(word):
    return _synonyms(_find_vector(word))

def _scrape_google(phrase,N = 3):
    # searches target word on google and returns N results as raw html
    search_term = '+'.join(phrase.split())
    results = get('https://www.google.com/search?q={}&num={}&hl=en'.format(search_term,N))
    return results.text

def _parse_html(html):
    soup= BeautifulSoup(html, 'html.parser')
    documents = []
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:
        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                documents.append(description)
    return documents

def search_internet(phrase):
    return _parse_html(_scrape_google(phrase))

w = 'malignant'
learn({w}) 
print(exact_meaning(w))
print(similar_meaning(w))
