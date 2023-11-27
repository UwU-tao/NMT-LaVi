import os
import regex

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

# remove emoji, html, links
emoji = r'(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])'
html  = r'<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|\'.*?\'|[\^\'\">\s]+))?)+\s*|\as*)\/?>'
link = r'([(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=-]{2,256}\.[a-z]{2,6}|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\b([-a-zA-Z0-9@:%_\+~#?&//=]*)'
def no_more_trash(file, out):
    with open(file,'r') as f, open(out,'w+') as f2:
        lines = f.readlines()
        for line in lines:
            # no emoji
            line = regex.sub(emoji,'',line)
            # no html tags
            line = regex.sub(html,'',line)
            # no links
            line = regex.sub(link,'',line)
            f2.write(line)

# create x lines version of train2023
def create_x_lines(x):
    file_lo = pre_processed + 'train2023.lo'
    file_vi = pre_processed + 'train2023.vi'

    with open(file_lo,'r') as flo, open(file_vi,'r') as fvi, open(pre_processed + f'train{x}.lo','w+') as flo2, open(pre_processed + f'train{x}.vi','w+') as fvi2:
        lines_lo = flo.readlines()
        lines_vi = fvi.readlines()
        n = min(len(lines_lo),len(lines_vi))
        for i in range(0,x):
            flo2.write(lines_lo[i])
            fvi2.write(lines_vi[i])
    print(f'Create {x} lines version done!')


for file in file_list:
    add_dot(raw + file, pre_processed + 'adddot_' + file)
print('Add dot done!')

for file in file_name:
    no_more_dup(pre_processed + 'adddot_' + file, pre_processed + 'nodup_' + file)
print('Remove duplicate done!')

for file in file_list:
    no_more_trash(pre_processed + 'nodup_' + file, pre_processed + file)
print('Remove trash done!')

create_x_lines(1000)
create_x_lines(10000)
create_x_lines(50000)