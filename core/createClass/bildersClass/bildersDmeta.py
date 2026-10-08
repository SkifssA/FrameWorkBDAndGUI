from dataclasses import dataclass, field, asdict
from dacite import from_dict, Config

from core.package.FileManager import FileManagerPkg
from .bilderBase import BilderBase
from core.dataClass.tabDataClass import tabShema, BASE_ATTR
from core.dataClass.metaDataClass import metaShema, attrMetaShema

class BildersDmeta(BilderBase):
    suffixFile = '.Dmeta.json'

    async def createFile(self, path):
        pathWhitFile = self._getPathAndFile(path)
        metaVisible = self.__getShowAttr()
        attrMeta = list(from_dict(data_class=attrMetaShema, data=i) for i in BASE_ATTR)
        for attr in self.data.attr:
            attrMeta.append(attrMetaShema(
                name=attr.name
                , caption=attr.caption
                , type=attr.type
                , editType=attr.editType
                , isVisible=attr.name in metaVisible
                , order=attr.order
                ))  
            if attr.name.startswith('id'):
                attrMeta.append(attrMetaShema(
                    name=attr.name+'HL'
                    , caption=attr.caption
                    , type=attr.type
                    , editType=attr.editType
                    , isVisible=attr.name+'HL' in metaVisible
                    , order=attr.order+0.1
                    , refTab=attr.refTab
                    , display='LookUp'
                    , attrId=attr.name
                ))

        formDefault = metaShema(
            name='Default'
            , caption=self.data.caption
            , isVisibleToolBar=True
            , attr=attrMeta
        )

        formList = metaShema(
            name='List'
            , typeForm='list'    
        )

        formCard = metaShema(
            name='Card'
            , typeForm='card'    
        )

        await FileManagerPkg.CreateFile(pathWhitFile, {'repres':[formDefault.getDict(), formList.getDict(), formCard.getDict()]})
        return {f'{self.data.name}{self.suffixFile}': pathWhitFile}

    def __getShowAttr(self):
        res = []
        for i in self.data.attr:
            if not i.isVisible:
                continue
            res.append(i.name+('HL' if i.name.startswith('id') else ''))
        return res