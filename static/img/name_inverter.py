import os
import json
# path = "./movie_image/"
path = "./tv_image/"
# path="./book_image/"
# print(os.listdir())
file_lst = os.listdir(path)

with open('./contents_idx.json', 'r') as f:
    name_idx = json.load(f)

name_idx = {v[:-1]:k for k,v in name_idx.items()}



def changeName(path, cName):
    i = 1
    for filename in os.listdir(path):
        
        try:
            print(path+filename, '=>', path+str(cName[filename[:-4]])+str(i)+'.jpg')
            os.rename(path+filename, path+str(cName[filename[:-4]])+str(i)+'.jpg')
        
        except:
            os.remove(path+filename)
        
        
        i += 1

changeName(path, name_idx)
# for file in file_lst:
#     filepath = path + '/' + file
#     print(file)