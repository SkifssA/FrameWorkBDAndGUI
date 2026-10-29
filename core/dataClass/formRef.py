from dataclasses import dataclass
from dacite import from_dict


CHR_SEPARATOR_PARENT = '.'
CHR_SEPARATOR_CLS = '/'

@dataclass
class FormRef:
    clsName: str
    subClsName: str

    @classmethod
    def createByStr(cls, value:str)->'FormRef':
        clsName, subClsName = value.split(CHR_SEPARATOR_CLS)
        return cls.create(clsName, subClsName)

    @classmethod
    def create(cls, clsName:str, subClsName:str)->'FormRef':
        return from_dict(data_class=cls, data={'clsName': clsName, 'subClsName': subClsName})

    def getStr(self)->str:
        return f'{self.clsName}{CHR_SEPARATOR_CLS}{self.subClsName}'