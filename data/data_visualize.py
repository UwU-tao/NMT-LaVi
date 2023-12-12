import matplotlib.pyplot as plt
import numpy as np

raw = '/home/huy/nlp/NMT-LaVi/data/raw/'
file_list_lo = ['dev2023.lo',
                'train2023.lo',
                'test.lo']
file_list_vi = ['dev2023.vi',
                'train2023.vi',
                'test.vi']
file_list = file_list_lo + file_list_vi
dup = '/home/huy/nlp/NMT-LaVi/data/dup/'
pre_processed = '/home/huy/nlp/NMT-LaVi/data/pre_processed/'
prepared = '/home/huy/nlp/NMT-LaVi/data/prepared/'
test = '/home/huy/nlp/NMT-LaVi/data/test/'


# file_list = ['train2023.lo','train2023.vi']
cnt = 1
for file in file_list:
    # with open(pre_processed + file,'r') as f:
    with open(pre_processed + file,'r') as f:
        print(file)
        line_len = dict()
        lines = f.readlines()
        for line in lines:
            if line_len.get(len(line)) == None:
                line_len[len(line)] = 1
            line_len[len(line)] += 1
        
        plt.subplot(2,3,cnt)
        cnt+=1
        keys = line_len.keys()
        values = line_len.values()
        plt.bar(keys, values)
        plt.title(file)
        # plt.hist(line_len,100)

plt.show()