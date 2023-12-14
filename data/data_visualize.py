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
# file_list = ['train40000.lo','train40000.vi']
# cnt = 1
# for file in file_list:
#     with open(pre_processed + file,'r') as f:
#     # with open(raw + file,'r') as f:
#         print(file)
#         line_len = dict()
#         lines = f.readlines()
#         for line in lines:
#             if line_len.get(len(line)) == None:
#                 line_len[len(line)] = 1
#             line_len[len(line)] += 1
#             if(len(line) > 600):
#                 print(line)
        
#         plt.subplot(1,2,cnt)
#         cnt+=1
#         keys = line_len.keys()
#         values = line_len.values()
#         plt.bar(keys, values)
#         plt.title(file)
#         # plt.hist(line_len,100)
# plt.show()


num_dup = [59, 19626] # duplicated lines
num_trash = [51, 2318] # lines have trash (not removed)
num_vie = [9, 165] # lines have vietnamese
num_trim = [106, 6020] # lines have length > 300
dev = [num_dup[0], num_trash[0], num_vie[0], num_trim[0],2000-num_dup[0]-num_trash[0]-num_vie[0]-num_trim[0]]
train = [num_dup[1], num_trash[1], num_vie[1], num_trim[1],100000-1500-num_dup[1]-num_trash[1]-num_vie[1]-num_trim[1]]
labels = ['Duplicate', 'Trash', 'Vietnamese', 'Length > 300','Remainings']
plt.subplot(1,2,1)
plt.pie(dev, autopct='%1.1f%%', startangle=90, counterclock=False, pctdistance= 1.1, explode=(0.1,0.1,0.1,0.1,0))
plt.title('dev2023')
plt.legend(labels, loc="best")

plt.subplot(1,2,2)
plt.pie(train, autopct='%1.1f%%', startangle=90, counterclock=False, pctdistance= 1.1, explode=(0.1,0.1,0.1,0.1,0))
plt.title('train2023')
# plt.legend()
plt.show()