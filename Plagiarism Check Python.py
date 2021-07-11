# 07/11/2021 by Seungho Jang

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
source_lst_re = []
test_lst = []
test_lst_re = []
results_lst = []
idx_check = []
ngram_lst = []
ngram_word_lst = []
n_ngram_lst = []
recall = 0
temp_i = 0
temp_j = 0
tb = dict()
check = 0
check_1 = ''
ngram = 0

for filename in source_arr:
    with open(os.path.join(source_path, filename), 'r', errors = 'replace') as fn:
        if filename.endswith('txt'):
            source_line = fn.readlines()
            for line in source_line:
                source_lst.extend(word_tokenize(line))

        # Lowercase
        source_lst = [token.lower() for token in source_lst]

        # Remove stopwords
        source_lst_re = Remove_stopwords(source_lst)

        # Remove punctuations
        source_lst_re = Remove_punct(source_lst_re)

print (source_lst [:30])

for filename in test_arr:
    with open(os.path.join(test_path, filename), 'r', errors = 'ignore') as fp:
        if filename.endswith('txt'):
            test_line = fp.readlines()
            
            for line in test_line:
                test_lst.extend(word_tokenize(line))

            # Lowercase
            test_lst = [token.lower() for token in test_lst]

            # Remove stopwords
            test_lst_re = Remove_stopwords(test_lst)

            # Remove punctuations
            test_lst_re = Remove_punct(test_lst_re)

            # Compare more than 3-gram words
            for i,v1 in enumerate(test_lst):
                for j,v2 in enumerate(source_lst):
                    if v1 == v2:
                        while i not in idx_check:
                            idx_check.append(i)
                            ngram_lst.append(v1)
                            check += 1
                    
                            temp_i = i+1
                            temp_j = j+1

                            try:
                                while test_lst[temp_i] == source_lst[temp_j]:
                                    idx_check.append(temp_i)
                                    ngram_lst.append(source_lst[temp_j])
                                    check +=1
                                    temp_i += 1
                                    temp_j += 1
                            except:
                                pass
                        
                            if check > 4:
                                #print(idx_check)
                                #print(ngram_lst)
                                ngram += 1
                                n_ngram_lst.append(len(ngram_lst))
                                ngram_word_lst.append(ngram_lst)
                            else:
                                ngram_lst = []
                                check = 0
                            
                            ngram_lst = []
                            check = 0
                        check = 0
                
            # Compare unique words
            for tlist in set(test_lst_re): 
                for slist in set(source_lst_re):
                    if slist == tlist:
                        recall += 1

            print(filename[:-4])
            print(ngram_word_lst)
    
            # Check Algorithm
    
            # 1)If similarity is over 50
            if (100*recall/len(set(test_lst_re))) >= 50:
                check_1 = "Check"

            # 2) If n_gram percentage is over 3
            elif (100*sum(n_ngram_lst)/len(test_lst)) >= 3:
                check_1 = "Check"

            # 3) If max in the list is over 7
            elif len(n_ngram_lst) > 0:
                if max(n_ngram_lst) >= 7:
                    check_1 = "Check"
                else:
                    check_1 = ""
            else:
                check_1 = ""

            tb.setdefault(0,[]).append(filename[:-4])
            tb.setdefault(1,[]).append(len(set(source_lst_re)))
            tb.setdefault(2,[]).append(len(set(test_lst_re)))
            tb.setdefault(3,[]).append("{:.2f}".format(100*len(set(test_lst))/len(test_lst_re)))
            tb.setdefault(4,[]).append(recall)
            tb.setdefault(5,[]).append("{:.2f}".format(100*recall/len(set(test_lst_re))))
            tb.setdefault(6,[]).append(ngram)
            tb.setdefault(7,[]).append(n_ngram_lst)
            tb.setdefault(8,[]).append("{:.2f}".format(100*sum(n_ngram_lst)/len(test_lst)))
            tb.setdefault(9,[]).append(check_1)
	
            # Create a Table
            #dt = pd.DataFrame(tb, columns = [0,1,2,3,4,5,6,7,8])
            dt = pd.DataFrame(tb, columns = [0,5,6,7,8,9])
    
            # Rename the columns for easy look
            #dt.columns=['Filename','Source Word Types', 'Word Types', 'Type/Token', 'Used Word Types from Source', 'Word Type Similarity Percentage','Number of 4 gram', 'length of 4 gram lists','lists/token percentage', 'check']

            # Actual Columns for 
            dt.columns=['Filename', 'Word Type Similarity Percent','Number of 4 gram', 'Length of 4 gram lists','Lists/token Percent', 'Check']
    
        # reset the recall, and test list
        recall = 0
        test_lst = []
        test_lst_re = []
        ngram = 0
        ngram_lst = []
        ngram_word_lst = []
        n_ngram_lst = []
        idx_check = []
        check_1 = 0
    
# Print
print(dt)   
print("\t")

# Print as csv
dt.to_csv("Plagiarism Check Results.csv", index = False)
