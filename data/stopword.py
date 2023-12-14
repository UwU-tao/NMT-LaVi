import laonlp
import re
import os
lao_stopwords = laonlp.lao_stopwords()
with open('data/vietnamese-stopwords.txt','r') as f:
    vietnamese_stopwords = f.read().split('\n')

pre_processed = '/home/huy/nlp/NMT-LaVi/data/pre_processed/'
file_list_lo = ['dev2023.lo',
                'train2023.lo']
file_list_vi = ['dev2023.vi',
                'train2023.vi']

def remove_stopwords(file, stopwords, laos = False):
    with open(pre_processed + file,'r') as f, open(pre_processed + 'stopwords_removed/' + file,'w+') as f2:
        lines = f.readlines()
        for line in lines:
            if laos == False:
                words = line.split()
            else:
                words = laonlp.tokenize.word_tokenize(line)
            words = [word for word in words if word not in stopwords]
            line = ' '.join(words)
            line = re.sub(' +', ' ', line)  # remove redundant spaces
            # check if line has endline character
            if line[-1] != '\n':
                line += '\n'
            f2.write(line)
    print(f'Remove stopwords from {file} done!')

# for file in file_list_lo:
#     remove_stopwords(file, lao_stopwords, True)
# for file in file_list_vi:
#     remove_stopwords(file, vietnamese_stopwords, False)


def check_length(file):
    with open(pre_processed + 'stopwords_removed/' + file,'r') as f:
        lines = f.readlines()
        for i in range(0,len(lines)):
            if len(lines[i]) > 400:
                print(file, i)

# del_lines = []
# os.rename(pre_processed + 'stopwords_removed/train2023.lo', pre_processed + 'stopwords_removed/train.lo')
# with open(pre_processed + 'stopwords_removed/train.lo','r') as f, open(pre_processed + 'stopwords_removed/train2023.lo','w+') as f2:
#     lines = f.readlines()
#     for i in range(0,len(lines)):
#         if len(lines[i]) > 400:
#             del_lines.append(i)
#         else:
#             f2.write(lines[i])

# os.rename(pre_processed + 'stopwords_removed/train2023.vi', pre_processed + 'stopwords_removed/train.vi')
# with open(pre_processed + 'stopwords_removed/train.vi','r') as f, open(pre_processed + 'stopwords_removed/train2023.vi','w+') as f2:
#     lines = f.readlines()
#     for i in range(0,len(lines)):
#         if i not in del_lines:
#             f2.write(lines[i])

# os.remove(pre_processed + 'stopwords_removed/train.lo')
# os.remove(pre_processed + 'stopwords_removed/train.vi')
                
for file in file_list_lo:
    check_length(file)
for file in file_list_vi:
    check_length(file)