import os
import re

# add '.' to end of all lines
def add_dot(file, out):
    with open(file,'r') as f, open(out,'w+') as f2:
        lines = f.readlines()
        for line in lines:
            if line[-2] != '.':
                line = line[:-1] + '.\n'
            f2.write(line)

# remove duplicate lines (in both la vi)
def no_more_dup(file, out):
    num_dup = 0
    with open(file + '.lo','r') as flo, open(file + '.vi','r') as fvi, open(out + '.lo','w+') as flo2, open(out + '.vi','w+') as fvi2:
        lines_lo = flo.readlines()
        lines_vi = fvi.readlines()
        n = min(len(lines_lo),len(lines_vi))
        line_set_lo = set()
        line_set_vi = set()
        for i in range(0,n):
            if((lines_lo[i] not in line_set_lo) and (lines_vi[i] not in line_set_vi)):
                line_set_lo.add(lines_lo[i])
                line_set_vi.add(lines_vi[i])
                flo2.write(lines_lo[i])
                fvi2.write(lines_vi[i])
            else:
                num_dup += 1
    return num_dup

# remove emoji, html, links
# emoji = r'(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])'
emoji = r'/<a?:.+?:\d{18}>|\p{Extended_Pictographic}/gu'
html  = r'<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|\'.*?\'|[\^\'\">\s]+))?)+\s*|\as*)\/?>'
link = r'([(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=-]{2,256}\.[a-z]{2,6}|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\b([-a-zA-Z0-9@:%_\+~#?&//=]*)'
def no_more_trash(file, out):
    num_trash = 0
    with open(file,'r') as f, open(out,'w+') as f2:
        lines = f.readlines()
        for line in lines:
            pre = len(line)
            # no emoji
            line = re.sub(emoji,'',line)
            # no html tags
            line = re.sub(html,'',line)
            # no links
            line = re.sub(link,'',line)
            f2.write(line)
            if len(line) != pre:
                num_trash += 1
    return num_trash

# remove lines with emoji, html, links
def no_more_trash_line(file, out):
    num_trash = 0
    with open(file + '.lo','r') as flo, open(file + '.vi','r') as fvi, open(out + '.lo','w+') as flo2, open(out + '.vi','w+') as fvi2:
        lines_lo = flo.readlines()
        lines_vi = fvi.readlines()
        n = min(len(lines_lo),len(lines_vi))
        for i in range(0,n):
            # if(re.search(emoji,lines_lo[i],re.IGNORECASE) != None) or (re.search(emoji,lines_vi[i],re.IGNORECASE) != None):
            #     num_trash += 1
            #     continue
            if(re.search(html,lines_lo[i],re.IGNORECASE) != None) or (re.search(html,lines_vi[i],re.IGNORECASE) != None):
                num_trash += 1
                continue
            if(re.search(link,lines_lo[i],re.IGNORECASE) != None) or (re.search(link,lines_vi[i],re.IGNORECASE) != None):
                num_trash += 1
                continue
            flo2.write(lines_lo[i])
            fvi2.write(lines_vi[i])
    return num_trash

# delete any case that Vi occure in La
vietnamese = r'[áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]'
def no_more_vi_in_lo(file, out):
    num_vie = 0
    with open(file + '.lo','r') as flo, open(file + '.vi','r') as fvi, open(out + '.lo','w+') as flo2, open(out + '.vi','w+') as fvi2:
        lines_lo = flo.readlines()
        lines_vi = fvi.readlines()
        n = min(len(lines_lo),len(lines_vi))
        for i in range(0,n):
            if(re.search(vietnamese,lines_lo[i],re.IGNORECASE) == None):
                flo2.write(lines_lo[i])
                fvi2.write(lines_vi[i])
            else:
                num_vie += 1
    return num_vie

# trim to only allow sen with len <= max length
def trim(length, file, out):
    num_trim = 0
    with open(file + '.lo','r') as flo, open(file + '.vi','r') as fvi, open(out + '.lo','w+') as flo2, open(out + '.vi','w+') as fvi2:
        lines_lo = flo.readlines()
        lines_vi = fvi.readlines()
        n = min(len(lines_lo),len(lines_vi))
        for i in range(0,n):
            if(len(lines_lo[i]) > length) or (len(lines_vi[i]) > length):
                num_trim += 1
                continue
            flo2.write(lines_lo[i])
            fvi2.write(lines_vi[i])
    return num_trim

# make punctuation to be separated by space
def sep_punc(file, out):
    with open(file,'r') as f, open(out,'w+') as f2:
        lines = f.readlines()
        for line in lines:
            # sepereate punctuation from words
            line = re.sub(r'([-_:;.,!?()])', r' \1 ', line)
            # remove multiple spaces
            line = re.sub(r'[" "]+', " ", line)
            f2.write(line)

# cut the final file in 2 parts: train and test - for infer
def cut_first_n_lines(n, file, outTest, outTrain):
    with open(file,'r') as f, open(outTest,'w+') as ft, open(outTrain,'w+') as ftr:
        lines = f.readlines()
        for i in range(0,n):
            ft.write(lines[i])
        for i in range(n,len(lines)):
            ftr.write(lines[i])

# create x lines version of train2023
def create_x_lines(filename, x):
    file_lo = filename + '.lo'
    file_vi = filename + '.vi'

    with open(file_lo,'r') as flo, open(file_vi,'r') as fvi, open(pre_processed + f'train{x}.lo','w+') as flo2, open(pre_processed + f'train{x}.vi','w+') as fvi2:
        lines_lo = flo.readlines()
        lines_vi = fvi.readlines()
        n = min(len(lines_lo),len(lines_vi))
        for i in range(0,x):
            flo2.write(lines_lo[i])
            fvi2.write(lines_vi[i])
    print(f'Create {x} lines version done!')

raw = '/home/huy/nlp/NMT-LaVi/data/raw/'
file_list_lo = ['dev2023.lo',
                'train2023.lo']
file_list_vi = ['dev2023.vi',
                'train2023.vi']
file_name = ['dev2023',     
             'train2023']
file_list = file_list_lo + file_list_vi
pre_processed = '/home/huy/nlp/NMT-LaVi/data/pre_processed/'
print('File list: ', file_list)

#DOT
for file in file_list:
    add_dot(raw + file, pre_processed + 'adddot_' + file)
print('Add dot done!')

#DUP
for file in file_name:
    num = no_more_dup(pre_processed + 'adddot_' + file, pre_processed + 'nodup_' + file)
    print('Removed dup in ', file, ': ', num)
print('Remove duplicate done!')

#TRASH
for file in file_name:
    num = no_more_trash_line(pre_processed + 'nodup_' + file, pre_processed + 'notrash_' + file)
    print('Removed trash in ', file, ': ', num)
print('Remove trash done!')

#VIETNAMESE
for file in file_name:
    num = no_more_vi_in_lo(pre_processed + 'notrash_' + file, pre_processed + 'no_vi_in_lo_' + file)
    # no_more_vi_in_lo(pre_processed + 'notrash_' + file, pre_processed + file)
    print('Removed vie in ', file, ': ', num)
print('Remove Vi in La done!')

# #SEP PUNC
for file in file_list:
    sep_punc(pre_processed + 'no_vi_in_lo_' + file, pre_processed + 'sep_' + file)

#TRIM
for file in file_name:
    num = trim(400, pre_processed + 'sep_' + file, pre_processed + file)
    print('Trimed in ', file, ': ', num)
print('Triming to max length done!')

# # cut first 1500 lines from train to make test file
# os.rename(pre_processed + 'train2023.lo', pre_processed + 'xtrain2023.lo')
# os.rename(pre_processed + 'train2023.vi', pre_processed + 'xtrain2023.vi')  
# cut_first_n_lines(1500, pre_processed + 'xtrain2023.lo', pre_processed + 'test.lo', pre_processed + 'train2023.lo')
# cut_first_n_lines(1500, pre_processed + 'xtrain2023.vi', pre_processed + 'test.vi', pre_processed + 'train2023.vi')

#delete all files except train2023 and dev2023
# file_list.append('test.lo')
# file_list.append('test.vi')
for file in os.listdir(pre_processed):
    if file not in file_list:
        os.remove(pre_processed + file)
print('File clean up done!')

# create_x_lines(1000)
# create_x_lines(10000)
# create_x_lines(50000)
# create_x_lines(raw + 'train2023', 40000)

            

# # create only laos, non latin sentence
# with open(pre_processed + 'train2023.lo','r') as flo, open(pre_processed + 'train2023.vi','r') as fvi, open(pre_processed + 'train.lo','w+') as flo2, open(pre_processed + 'train.vi','w+') as fvi2:
#     lines_lo = flo.readlines()
#     lines_vi = fvi.readlines()
#     n = min(len(lines_lo),len(lines_vi))
#     for i in range(0,n):
#         if(re.search(vietnamese,lines_lo[i],re.IGNORECASE) == None):
#             flo2.write(lines_lo[i])
#             fvi2.write(lines_vi[i])
#         else:
#             if i < 10000:
#                 print(i,re.search(vietnamese,lines_lo[i],re.IGNORECASE),re.search(r'[a-zA-Z0-9]',lines_lo[i]))