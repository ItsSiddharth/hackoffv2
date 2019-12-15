import pickle
from gensim.models.keyedvectors import KeyedVectors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import subprocess
import time

start = time.time()

class video_search:

    def load_model(self):
        modelname = 'glove_model.pickle'
        infile = open(modelname,'rb')
        glove_model = pickle.load(infile)
        infile.close()
        return glove_model

    def pass_json_for_getting_list(self, filepath='data.json'):
        with open(filepath) as transcribe:
            dat=json.load(transcribe)
        all_words = []
        n=(len(dat['results']['items']))
        a=dat['results']['items']
        for i in range(0,n):
            b=[]
            b.append(a[i]["alternatives"][0]["content"])
            try:
                b.append(float(a[i]["start_time"]))
                b.append(float(a[i]["end_time"]))
                all_words.append(b)
            except:
                continue

        return all_words
        
    def filtering_list(self, all_words):
        filtered_list = []
        for word in all_words:
            example_sent = word[0]
            stop_words = set(stopwords.words('english')) 
            word_tokens = word_tokenize(example_sent) 
            for w in word_tokens: 
                if w not in stop_words: 
                    filtered_list.append([w,word[1],word[2]])
        return filtered_list
        
    def algorithm (self, filtered_list, input_word, model):
        pos,counter = [],[]
        distance, count = 0, 0
        for element in filtered_list:
            word = element[0] 
            if word == input_word:
                pos.append(count)
            count = count + 1
        for i in range (0,len(pos)-1):
            for j in range (pos[i]+1,pos[i+1]):
                try:
                    distance = distance + glove_model.similarity(filtered_list[j][0],input_word)
                except:
                    pass
            counter.append(distance/j)
            distance = 0
            maximum_value = max(counter)
            return (filtered_list[pos[counter.index(maximum_value)]][1])

test = video_search()
#print(test.algorithm(test.filtering_list(test.pass_json_for_getting_list()), 'module', test.load_model()))
#print(time.time() - start)



        
