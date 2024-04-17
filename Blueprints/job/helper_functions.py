def str_to_list(str):
    if str == '[]':
        return []
    
    str = str[1:-1]
    lst = str.split(', ')
    return lst