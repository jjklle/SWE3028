import numpy as np
import csv

f = open('./user_preference.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)

numRow = 0
for column in rdr:
    if numRow == 0 :
        columnNames = column
    numRow += 1
numCol = len(columnNames)

numUsers = numRow - 1
dim = numCol - 2
users = np.empty([numUsers,numCol],dtype=np.str_)

f = open('./user_preference.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)

i = 0
for column in rdr:
    if i != 0 :
        users[i-1] = column
        
    i += 1
f.close()
user_id = users[:,1]
bitVectors = np.empty(numUsers,dtype=object)

for n in range(0,numUsers) :
    bitVector = users[n,2:]

    #bitVector to bitVector2str
    bitVector2str = ""
    for i in range (0, dim) :
        bitVector2str += bitVector[i]
    bitVectors[n] = bitVector2str

f = open('user_preference_preprocessed.csv', 'w', newline='')
wr = csv.writer(f)
wr.writerow(["","user_id","bit_vector"])
for i in range (0,numUsers) :
    wr.writerow([str(i),user_id[i],bitVectors[i]])

'''
#bitVector2str to bitVector_
bitVector_ = np.empty(dim, dtype=np.str_)
for i in range (0, dim) :
    bitVector_[i] = bitVector2str[i]
'''