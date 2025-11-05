
def SetFilter(sqlWhere: str, label: str = None, order:int=0, typeEdit:str='check'):
    def decorator(func):
        filter_id = func.__name__
        func._is_filter_handler = True
        func._filter_label = label or filter_id.replace('_', ' ').title()
        func._filter_id = filter_id
        func._order = order
        func._where = sqlWhere
        func._typeEdit = typeEdit
        return func
    return decorator