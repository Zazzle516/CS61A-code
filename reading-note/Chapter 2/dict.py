def make_dict():
    """
    Return a function implenmentation of dictionary
    """
    record = []

    def getitem(key):
        for k,v in record:
            if k == key:
                return v
    
    def setitem(key,value):
        for pair in record:
            if(pair[0] == key):
                pair[1] = value
                return
        record.append([key,value])

    def dispatch(message, key = None , value = None):
        if message == 'getitem':
            return getitem(key)
        elif message == 'setitem':
            return setitem(key,value)
        elif message == 'keys':
            return tuple(k for k , _ in record)
        elif message == 'values':
            return tuple(v for _ , v in record)
        
    return dispatch