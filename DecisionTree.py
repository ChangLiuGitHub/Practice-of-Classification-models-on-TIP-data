#!/usr/bin/python3

import numpy as np
import csv
import sys
import fileinput
from sklearn import tree	
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import matplotlib.pyplot as plt 

flag=[]
label=[]
datas=[]
ids=[]

#load all data
f = open('%s' % sys.argv[1],'rU')
for row in f:
  cells = row.split(',',3)
  flag.append(cells[0].strip('"'))
  label.append(cells[1].strip('"'))
  ids.append(cells[2].strip('"'))
  feature_line=[float(x.strip('\n').strip('"')) for x in cells[3].split(',')]
  datas.append(feature_line)
f.close()


Trn_X=[]
Trn_y=[]
Trn_y_name=[]
Test_X=[]
Test_y_name=[]
Test_y=[]

#split trainning data and testing data and add target ID
for i in range(len(label)):
  if flag[i]=='train':
    Trn_X.append(datas[i])
    Trn_y_name.append(label[i])
    Trn_y.append(ids[i])
  else:
    Test_X.append(datas[i])
    Test_y_name.append(label[i])
    Test_y.append(ids[i])

targetID=[]
for i in range(len(Trn_y)):
  targetID.append('class '+str(i))

Trn_y =np.array(Trn_y)
Trn_X =np.array(Trn_X)
print ('Training X shape is ',Trn_X.dtype,Trn_X.shape)
Test_y =np.array(Test_y)
Test_X =np.array(Test_X)
print ('Testing X shape is ',Test_X.shape)
print ('Testing y is ',Test_y)

for crit in ['gini', 'entropy']:
  for spli in ['best', 'random']:
    for maxf in [5,10,100,None,'auto']:
      n=10
      sum_precision=0
      sum_recall=0
      sum_F1=0
      j=0
      while (j<n):
        #apply model
        clf = tree.DecisionTreeClassifier(criterion=crit, splitter=spli, max_features=maxf)
        clf = clf.fit(Trn_X,Trn_y)
        Pred_y = clf.predict(Test_X)
        #print ('Predicted y is ',Pred_y)
      
        #compute precision
        precision = precision_score(Test_y, Pred_y, average='micro')
        #print (' precision is ', precision)
        sum_precision = sum_precision + precision
        #compute recall
        recall = recall_score(Test_y, Pred_y, average='micro') 
        #print (' recall is ', recall)
        sum_recall = sum_recall + recall
        #compute F1 measure
        F1 = f1_score(Test_y, Pred_y, average='micro') 
        #print (' F1 is ', F1)
        sum_F1 = sum_F1 + F1
        print (crit, ' ', spli, ' ', maxf, ' precision is ', precision, ' recall is ', recall, ' F1 is ', F1)
        j=j+1
      
      print ('mean_precision is ', sum_precision/n)
      print ('mean_recall is ', sum_recall/n)
      print ('mean_F1 is ', sum_F1/n)
      
      #print (classification_report(Test_y, Pred_y, target_names=targetID))
