import dearpygui.dearpygui as dpg
import asyncio
import inspect

class Filter:
    def __init__(self, parent):
        self.tagInput = {}
        self.where = []
        with dpg.group(parent=parent.tab, 
                       horizontal=True) as fileter:
            self.tag = fileter
            if 'filter' in parent.meta:
                flt = parent.meta['filter']
                for i in flt:
                    self.where.append(i['where'])
                    for j in i['attr']:
                        show = i['attr'][j]['isVisible'] if 'isVisible' in i['attr'][j] else True
                        with dpg.child_window(border=False, 
                                              height=20, 
                                              width=-1, 
                                              show=show):
                            with dpg.group(horizontal=True):
                                with dpg.child_window(width=len(i['attr'][j]['caption'])*11,
                                                       border=False):
                                    dpg.add_text(i['attr'][j]['caption'])
                                if i['attr'][j]['edit'] == 'edit':
                                    self.tagInput[j] = dpg.add_input_text(width=-1, 
                                                                          callback=self.__getMetod(getattr(parent, f'set{j}', None)), 
                                                                          on_enter=True)

    def getWhere(self):
        return '\n and'.join(self.where)

    def _getAttr(self, nameAttr):
        return dpg.get_value(self.tagInput[nameAttr])
    
    def __getMetod(self, attr):
        if inspect.iscoroutinefunction(attr):
            return lambda: asyncio.run(attr())
        elif callable(attr):
            return attr



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