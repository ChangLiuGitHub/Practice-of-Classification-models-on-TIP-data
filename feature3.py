#!/usr/bin/python3
import numpy as np
import csv
import sys
import fileinput
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

flag=[]
label_1=[]
label_2=[]
label_3=[]
label_4=[]
descrip=[]
origs = []
removed=[]

def filter_alpha(line):
  newline = ""
  for ch in line:
    if ch.isalpha():
      newline = newline + ch
    else:
      newline = newline + ' '+ ch +' '
  return newline

#clean training data
f = open('%s' % sys.argv[1],'rU')
for row in f:
  cells = row.split(',',6)
  label_1.append(cells[1])
  label_2.append(cells[3])
  label_3.append(cells[4])
  label_4.append(cells[5])
  orig = cells[6]
  words = []
  remove = []
  for w in filter_alpha(orig).split():
    if len(w) >= 3:
      words.append(w)
    else:
      remove.append(w)
  descrip.append(' '.join(words))
  flag.append('train')

  origs.append(orig)
  removed.append(' '.join(remove))
f.close()

#clean testing data
f = open('%s' % sys.argv[2],'rU')
for row in f:
  cells = row.split(',',2)
  ##label_4.append(cells[0])
  label_2.append(cells[0])
  orig = cells[2]
  words = []
  remove = []
  for w in filter_alpha(orig).split():
    if len(w) >= 3:
      words.append(w)
    else:
      remove.append(w)
  descrip.append(' '.join(words))
  flag.append('test')

  origs.append(orig)
  removed.append(' '.join(remove))
f.close()


#save all removed
with open('%s-removed' % sys.argv[1],'w',newline='') as newfile:
  writer = csv.writer(newfile,delimiter=',',quoting=csv.QUOTE_ALL)
  writer.writerow(['label', 'original', 'removed', 'kept'])
  for i in range(len(label_2)):
    row=[label_2[i],origs[i],removed[i],descrip[i]]
    writer.writerow(row)

#record the 3 columns table which is ready for getting features
with open('%s' % sys.argv[3],'w',newline='') as newfile:
  writer = csv.writer(newfile,delimiter=',',quoting=csv.QUOTE_ALL)
  for i in range(len(label_2)):
    row=[flag[i],label_2[i],descrip[i]]
    writer.writerow(row)

##labels=np.array(label_4)
labels=np.array(label_2)
datas=np.array(descrip)

true_k=np.unique(labels).shape[0]

vectorizer = TfidfVectorizer(max_df=0.5, min_df=2,stop_words='english')

tfidf = vectorizer.fit_transform(datas)
tfidf_matrix=tfidf.toarray()
feature_names =vectorizer.get_feature_names()

print (feature_names,len(feature_names))
print (tfidf_matrix.shape)

#record the featured table
with open('%s' % sys.argv[4],'w',newline='') as featurefile:
  writer = csv.writer(featurefile,delimiter=',',quoting=csv.QUOTE_ALL)
  title = ['flag']+['label']+ [x for x in feature_names]
  writer.writerow(title)
  ##for i in range(len(label_4)):
  ##  row=[flag[i]] + [label_4[i]] + [x for x in tfidf_matrix[i]]
  for i in range(len(label_2)):
    row=[flag[i]] + [label_2[i]] + [x for x in tfidf_matrix[i]]
    writer.writerow(row)
