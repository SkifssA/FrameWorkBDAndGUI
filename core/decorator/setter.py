SETTER = 'setter'

def Setter():
    def decorator(func):
        func._is_type = SETTER
        func._oper_id = func.__name__
        return func
    return decorator