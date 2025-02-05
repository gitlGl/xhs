import os ,fnmatch,gzip, bz2, re
def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree 
    that match a shell wildcard pattern
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration. 
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

if __name__ == '__main__':
    #在www文件夹中寻找文件名前缀
    # 为access-log的所有文件
    lognames = gen_find('access-log*', 'www')
    files = gen_opener(lognames)
    lines = gen_concatenate(files)
    
    #这个正则表达式会匹配 "python"、"Python"、"PYTHON" 
    # 等任何大小写组合的 "python" 字符串。
    pylines = gen_grep('(?i)python', lines)
    for line in pylines:
        print(line)

   