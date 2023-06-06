# 在所在文件夹下运行
# 用来把行人标注去掉的 请无视
import os
path = "./labels/"
for i in os.listdir(path):
    i = path + i
    with open(i,'r',encoding='utf-8') as f:
        data = f.readlines()
        print(data)
        lst = []
        for line in data:
            if line[0] == '0':
                lst.append(line)
    print(lst)
    with open(i,'w',encoding='utf-8') as f:
        f.writelines(lst)