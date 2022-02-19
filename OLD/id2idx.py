import os, json

cwd = os.getcwd()
user_dir  =os.path.join(cwd,"Data_dup")
users = sorted([file.split(".csv")[0] for file in os.listdir(user_dir)])

id2idx = {}
for idx, user in enumerate(users):
    id2idx[idx] = user
    os.rename(os.path.join(user_dir, user+".csv"), os.path.join(user_dir, "P"+ str(idx).zfill(2) +".csv"))
with open("id2idx.json",'w+') as f:
    json.dump(id2idx,f)