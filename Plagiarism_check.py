# 06/15/2021 by Seungho Jang

import string
import numpy as np
import pandas as pd
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Remove stopwords function
def Remove_stopwords (s_list):
    stop_words = set(stopwords.words('english'))
    filtered_words=[]
    for i in s_list:
        if i not in stop_words:
            filtered_words.append(i)

    return filtered_words

# Remove Punctuation
def Remove_punct (s_list):
    punct = set(string.punctuation)
    filtered_words=[]
    for i in s_list:
        if i not in punct:
            filtered_words.append(i)

    return filtered_words

# Read files and Make a list of all 1-gram

source_path = 'Source'
test_path = 'Data'

source_arr = os.listdir(source_path)
test_arr = os.listdir(test_path)
strtxt = ".txt"

source_lst = []
test_lst = []
results_lst = []
recall = 0
tb = dict()

for filename in source_arr:
    with open(os.path.join(source_path, filename), 'r') as fn:
       source_line = fn.readlines()
       for line in source_line:
           source_lst.extend(word_tokenize(line))

    # Lowercase
    source_lst = [token.lower() for token in source_lst]

    # Remove stopwords
    source_lst = Remove_stopwords(source_lst)

    # Remove punctuations
    source_lst = Remove_punct(source_lst)

#print (source_lst [:50])

for filename in test_arr:
    with open(os.path.join(test_path, filename), 'r') as fp:
        test_line = fp.readlines()
        for line in test_line:
           test_lst.extend(word_tokenize(line))

    # Lowercase
    test_lst = [token.lower() for token in test_lst]

    # Remove stopwords
    test_lst = Remove_stopwords(test_lst)

    # Remove punctuations
    test_lst = Remove_punct(test_lst)

    # Compare
    # Test code for test_list
    #print (test_lst [:50])

    for tlist in set(test_lst): 
        for slist in set(source_lst):
            if slist == tlist:
                recall += 1

    tb.setdefault(0,[]).append(filename[:-4])
    tb.setdefault(1,[]).append(len(set(source_lst)))
    tb.setdefault(2,[]).append(len(set(test_lst)))
    tb.setdefault(3,[]).append(100*len(set(test_lst))/len(test_lst))
    tb.setdefault(4,[]).append(recall)
    tb.setdefault(5,[]).append(100*recall/len(set(test_lst)))

    # Create a Table
    dt = pd.DataFrame(tb, columns = [0,1,2,3,4,5])
    
    # Rename the columns for easy look
    dt.columns=['Filename','Uniq Source', 'Uniq Tes', 'Uniq/total word (Test)', 'Used Uniq Words from Source', 'Percentage']

    # reset the recall, and test list
    recall = 0
    test_lst = []

# Print
print(dt)   
print("\t")

# Print as csv
dt.to_csv("Plagiarism Check Results.csv", index = False)