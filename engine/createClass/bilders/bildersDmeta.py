from ...package import FileManagerPkg
from .bilderBase import BilderBase

class BildersDmeta(BilderBase):
    suffixFile = '.Dmeta.json'

    baseAttr = {
        'id': {
                'caption': 'id',
                'edit': 'edit',
                'isVisible': False,
                'order': -2
            },
        'gid': {
                'caption': 'gid',
                'edit': 'edit',
                'isVisible': False,
                'order': -1
            }
        }
    
    baseForm =  {'Default':{
            'caption': None,
            'isVisibleToolBar': True,
            'attr': []
        }}

    def __init__(self, data):
        super().__init__(data)
        self.form = self.baseForm.copy()
        self.form['Default']['caption'] = self.data['caption']
        self.data['showAttr'] = self.__getShowAttr()

    async def createFile(self, path):
        pathWhitFileD = self._getPathAndFile(path)
        attr = {}
        for i in self.data['attr']:
            attr[i['name']] = {
                    "caption": i['caption'],
                    "edit": i.get('editType', 'edit'),
                    'isVisible': i['name'] in self.data['showAttr'],
                    'order': i.get('order', 0)
                }
            if i['name'].startswith('id'):
                attr[i['name']+'HL'] = {
                    "caption": i['caption'],
                    "edit": i['editType'] if 'editType' in i else 'button',
                    'isVisible': i['name']+'HL' in self.data['showAttr'],
                    'order': i.get('order', 0),
                    'refTab': i['refTab'],
                    'display': i.get('display', 'list')
                }
                attr[i['name']]['edit'] = 'edit'
            if  'editType' in i:
                if i['editType'] == 'lookUp':
                    attr[i['name']+'HL']['display'] = 'LookUp'
                    attr[i['name']+'HL']['refTab'] = i['refTab']
                    attr[i['name']+'HL']['order'] = i.get('order', 0)+0.1

        self.form['Default']['attr'] = {**self.baseAttr, **attr} 

        await FileManagerPkg.CreateFile(pathWhitFileD, self.form)

    def __getShowAttr(self):
        res = []
        for i in self.data['attr']:
            if 'isVisible' in i:
                if not i['isVisible']:
                    continue
            res.append(i['name']+('HL' if i['name'].startswith('id') else ''))
        return res