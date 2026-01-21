from ...package import Core_FileManagerPkg
from .bilderBase import BilderBase

class BildersDmeta(BilderBase):
    suffixFile = '.Dmeta.json'

    baseAttr = {
        'id': {
                'caption': 'id',
                'edit': 'edit',
                'isVisible': False
            },
        'gid': {
                'caption': 'gid',
                'edit': 'edit',
                'isVisible': False
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
                    "edit": i['editType'] if 'editType' in i else 'edit',
                    'isVisible': i['name'] in self.data['showAttr']
                }
            if i['name'].startswith('id'):
                attr[i['name']+'HL'] = {
                    "caption": i['caption'],
                    "edit": i['editType'] if 'editType' in i else 'edit',
                    'isVisible': i['name']+'HL' in self.data['showAttr']
                }
                attr[i['name']]['edit'] = 'edit'
            if  'editType' in i:
                if i['editType'] == 'lookUp':
                    attr[i['name']+'HL']['display'] = 'LookUp'
                    attr[i['name']+'HL']['refTab'] = i['refTab']

        self.form['Default']['attr'] = {**self.baseAttr, **attr} 

        await Core_FileManagerPkg.CreateFile(pathWhitFileD, self.form)

    def __getShowAttr(self):
        res = []
        for i in self.data['attr']:
            if 'isVisible' in i:
                if not i['isVisible']:
                    continue
            res.append(i['name']+('HL' if i['name'].startswith('id') else ''))
        return res