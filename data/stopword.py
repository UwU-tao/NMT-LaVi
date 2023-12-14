import laonlp
import re
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
            f2.write(line + '\n')
    print(f'Remove stopwords from {file} done!')

for file in file_list_lo:
    remove_stopwords(file, lao_stopwords, True)
for file in file_list_vi:
    remove_stopwords(file, vietnamese_stopwords, False)
        