import os
import json
# path = "./movie_image2/"
# path = "./tv_image/"
path="./book_image/"
# print(os.listdir())
file_lst = os.listdir(path)

with open('./contents_idx.json', 'r') as f:
    name_idx = json.load(f)

name_idx = {v[:-1]:k for k,v in name_idx.items()}



def changeName(path, cName):
    i = 1
    for file in os.listdir(path):
        colons = file.replace('--',':')
        slash = colons.replace('$', '/')
        star = slash.replace('@','?')
        bar = star.replace('%','|')
        file_name = bar.replace('##','*')
        try:
            os.rename(path+file, path+file_name)
        except:
            file
            print("special err")
        
        try:
            print(path+file_name, '=>', path+str(cName[file_name[:-4]])+str(i)+'.jpg')
            os.rename(path+file_name, path+str(cName[file_name[:-4]])+str(i)+'.jpg')
        
        except:
            # os.remove(path+filename)
            try:
                os.rename(path+file, path+str(cName[file_name[:-4]])+str(i)+'.jpg')
            except:
                print("", end="")
            
        
        
        i += 1

changeName(path, name_idx)
# for file in file_lst:
#     filepath = path + '/' + file
#     print(file)