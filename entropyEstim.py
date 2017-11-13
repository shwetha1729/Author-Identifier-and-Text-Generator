import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
import math
import random

### 1 - 2 ###
print("############ 1 - 2 ############")
books = ['melville-moby_dick.txt', 'austen-emma.txt', 'whitman-leaves.txt']

for i in books:
	x = nltk.corpus.gutenberg.words(i)
	print(i, len(x))

### 3 - start ###
print("############ 3 ############")
def generate_model(book, gram):
	text = nltk.corpus.gutenberg.words(book)
	model = ngrams(text, gram)
	freq = dict(Counter(model))
	return freq

models = {} 
for i in books:
	u = generate_model(i, 1)
	b = generate_model(i, 2)
	t = generate_model(i, 3)
	lst = []
	lst.append(u)
	lst.append(b)
	lst.append(t)
	models[i] = lst

l = ['Unigram model', 'Bigram model', 'Trigram model']
for i in books:
    print("----", i, "----")
    for j in range(3):
        d = models[i][j]
        print(l[j], ":")
        print("Types:", len(d), "; Tokens:", sum(d.values()))

def generate_prob(book, gram):
	res = {}
	d = models[book][gram - 1]
	if gram == 1:
		tot = sum(d.values())
		for i in d:
			res[i] = d[i] / tot

	else:
		for i in d:
			find = i[:gram - 1]
			tot = models[book][gram - 2][find]
			res[i] = d[i] / tot
	return res

prob = {}
for i in books:
	u = generate_prob(i, 1)
	b = generate_prob(i, 2)
	t = generate_prob(i, 3)
	lst = []
	lst.append(u)
	lst.append(b)
	lst.append(t)
	prob[i] = lst

import random
for i in books:
    print("From Unigram model of", i, random.choice(list(prob[i][0].items())))
    print("From Bigram model of", i, random.choice(list(prob[i][1].items())))
    print("From Trigram model of", i, random.choice(list(prob[i][2].items())))
### 3 - end ###

### 4 - start ###
print("############ 4 ############")

def random_sentence(book, gram, now):
	gen = ""
	d = models[book][gram - 1]
	for i in range(500):
		possible = list()
		for i in d:
			if(i[0 : len(i) - 1] == now):
				possible.append(i)
		nex = random.choice(possible)
		now = nex[1:]
		gen = gen + ' ' + nex[len(i) - 1]
	gen = gen.strip()
	return gen

def generate_entropy(book, gram, now):
	d = prob[book][gram - 1]
	text = random_sentence(book, gram, now)
	text = text.split()    
	model = ngrams(text, gram)
	model = list(model)
	ans = 0
	for i in model:
		temp = d[i]    
		ans = ans + math.log(temp, 2) 
	ans = ans * -1 / gram
	return ans

cross_entropy = {}
for i in books:
	u = generate_entropy(i, 1, ())
	b = generate_entropy(i, 2, ('.',))
	t = generate_entropy(i, 3, ('.', 'The'))

	lst = []
	lst.append(u)
	lst.append(b)
	lst.append(t)
	cross_entropy[i] = lst

print(cross_entropy)


l = ['Unigram model', 'Bigram model', 'Trigram model']
print("Cross Entropy Values -")
for i in books:
    print("----", i, "----")
    for j in range(3):
        print(l[j], ":", cross_entropy[i][j])
### 4 - end ###


### 5 - start ###
print("############ 5 ############")
sentence = list()
text = nltk.corpus.gutenberg.sents('austen-emma.txt')
sents = text[100:125]
for i in sents:
	for j in i:
		sentence.append(j)

def check_book(book, gram):
	ans = 0
	m = ngrams(sentence, gram)
	x = list(m)
	d = prob[book][gram - 1]
	for i in x:
		if i in d:
			y = int(math.log(d[i], 2))
			ans = ans + y
		else:
			ans = 0
			break
	return ans


book_prob = {}
for i in books:
	u = check_book(i, 1)
	b = check_book(i, 2)
	t = check_book(i, 3)

	lst = []
	lst.append(u) ## -1 * u
	lst.append(b)
	lst.append(t)

	book_prob[i] = lst

print(book_prob)

for i in books:
	d = book_prob[i]
	if d[0] != 0:
		print(i)

for i in books:
	d = book_prob[i]
	if d[0] != 0:
		print("Text belongs to book", i)
### 5 - end ###

### 6 -start ###
print("############ 6 ############")
def random_sentence_2(book, gram, now):
	gen = ""
	d = models[book][gram - 1]
	for i in range(100):
		possible = list()
		for i in d:
			if(i[0 : len(i) - 1] == now):
				possible.append(i)
		nex = random.choice(possible)
		now = nex[1:]
		gen = gen + ' ' + nex[len(i) - 1]
	gen = gen.strip()
	return gen

def generate_entropy_2(book, gram, now):
	d = prob[book][gram - 1]
	text = random_sentence_2(book, gram, now)
	text = text.split()    
	model = ngrams(text, gram)
	model = list(model)
	ans = 0
	for i in model:
		temp = d[i]       
		ans = ans + (math.log(temp, 2))
	return -1 * ans / gram

entropy = {}
for i in books:
	u = generate_entropy_2(i, 1, ())
	b = generate_entropy_2(i, 2, ('.',))
	t = generate_entropy_2(i, 3, ('.', 'The'))

	lst = []
	lst.append(u)
	lst.append(b)
	lst.append(t)
	entropy[i] = lst

print(entropy)

l = ['Unigram model', 'Bigram model', 'Trigram model']
for i in books:
    d = entropy[i]
    best = d.index(min(d))
    print("Most similar model to the original text of", i, "is", l[best])
### 6 - end ###
