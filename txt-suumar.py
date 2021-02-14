# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 22:22:23 2020

@author: rajpu
"""

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer

import glob

files = [open(file) for file in glob.glob("C:\\Users\\rajpu\\Desktop\\data\\nlp\\COVID_19_dataset\\documents\\*")]

text =[]
for f in files:
    t1= f.read()
    text.append(t1)
    f.close()
    
master_text = ""
for i in text:
    master_text = master_text +  "\n" + i
    
sent_token = nltk.sent_tokenize(master_text)
word_token = nltk.word_tokenize(master_text)

#STOPWORDS
word_tokens_lower = [ word.lower() for word in word_token]

stopWords = stopwords.words('english')

word_token_refined = [ word for word in word_tokens_lower if word not in stopWords]

#Lemmatization
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
lm = WordNetLemmatizer()
lem = []
for word in word_token_refined:
    lem.append(lm.lemmatize(word))
word_token_refined = lem

print(len(word_token))
print(len(word_token_refined))

#PorterStemmer
ps = PorterStemmer()
stem = []
for word in word_token_refined:
    stem.append(ps.stem(word))
word_token_refined = stem

#Frequency Distribution
from nltk.probability import FreqDist
fdist = FreqDist(word_token_refined)
#print(fdist)
import matplotlib.pyplot as plt
fdist.plot(50,cumulative=False)
plt.show()

FreqTable={}
for word in word_token_refined:
    if word in FreqTable:
        FreqTable[word]+=1
    else:
        FreqTable[word]=1


sent_value= {}

for sent in sent_token:
    sent_value[sent] = 0
    for word,freq in FreqTable.items():
        if word in sent.lower():
            sent_value[sent] = sent_value[sent] + freq
            
sum = 0
for sent in sent_value:
    sum +=sent_value[sent]
avg = int(sum/len(sent_value))

summary = ""


for sent in sent_value:
    if (sent_value[sent] >= 1.2*avg):
        summary = summary + " " + sent


count=0
who_verdict = ""
for sent in sent_value:
    if ("WHO" in sent):
        if (sent_value[sent] >= 1.2*avg):
            who_verdict = who_verdict + "\n" + sent
            count +=1
          

quest = "what is WHO's statement on COVID-19?"
answer = who_verdict
        
            
new_file = open("summary.txt","x")
new_file.write(summary)
new_file.close()    
