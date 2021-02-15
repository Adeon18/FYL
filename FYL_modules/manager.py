'''
A module that manages file reading
'''


def read_file(file_path='data/short.list'):
    '''
    Reads file, short.list by default.
    '''
    data = ''
    with open(file_path, 'r', encoding="utf8", errors='ignore') as file:
        data = file.read().split('\n')[14:-1]
    
    return tuple(set(data))
