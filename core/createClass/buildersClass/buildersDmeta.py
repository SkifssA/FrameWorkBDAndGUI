from dataclasses import dataclass, field, asdict
from dacite import from_dict, Config

from core.package.FileManager import FileManagerPkg
from .builderBase import builderBase
from core.dataClass.tabDataClass import tabSchema, BASE_ATTR
from core.dataClass.metaDataClass import metaSchema, attrMetaSchema


class buildersDmeta(builderBase):
    suffixFile = ".Dmeta.json"

    def createFile(self, path):
        pathWhitFile = self._getPathAndFile(path)
        metaVisible = self.__getShowAttr()
        attrMeta = list(from_dict(data_class=attrMetaSchema, data=i) for i in BASE_ATTR)
        for attr in self.data.attr:
            attrMeta.append(
                attrMetaSchema(
                    name=attr.name,
                    caption=attr.caption,
                    type=attr.type,
                    editType=attr.editType,
                    isVisible=attr.name in metaVisible,
                    order=attr.order,
                )
            )
            if attr.name.startswith("id"):
                attrMeta.append(
                    attrMetaSchema(
                        name=attr.name + "HL",
                        caption=attr.caption,
                        type=attr.type,
                        editType=attr.editType,
                        isVisible=attr.name + "HL" in metaVisible,
                        order=attr.order + 0.1,
                        refTab=attr.refTab,
                        display="LookUp",
                        attrId=attr.name,
                    )
                )

        formDefault = metaSchema(
            name="Default",
            caption=self.data.caption,
            isVisibleToolBar=True,
            attr=attrMeta,
        )

        formList = metaSchema(name="List", typeForm="list")

        formCard = metaSchema(name="Card", typeForm="card")

        FileManagerPkg.CreateFile(
            pathWhitFile,
            {"repres": [formDefault.getDict(), formList.getDict(), formCard.getDict()]},
        )

    def __getShowAttr(self):
        res = []
        for i in self.data.attr:
            if not i.isVisible:
                continue
            res.append(i.name + ("HL" if i.name.startswith("id") else ""))
        return res
