from .builderBase import builderBase


class builderDpi(builderBase):
    # Канонический шаблон Dpi-слоя. Golden-тесты tests/core/test_sc_golden.py
    # сверяют текст этого шаблона с эталонными файлами core/module/sc/**/*Dpi.py
    # (Sc_ClsDpi / Sc_ScriptsDpi). Меняешь шаблон — обнови эталоны и наоборот.
    temp = """# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
{imports}from dataclasses import dataclass
from typing import Optional

@dataclass
class {name}Obj(EmptyObj):
{attrLines}

class {name}Dpi(EmptyLogic[{name}Obj]):
    _classObj = {name}Obj
    _attrForHL = [\'{attrForHL}\']
    _attrForMC = [\'{attrForMC}\']

    def _getNameClass(self):
        return "{name}"

    def calcHeadLine(self, rop:{name}Obj)->str:
        return f'{headLine}'

    def calcMnemoCode(self, rop:{name}Obj)->str:
        return f'{mnemoCode}'

{deleteDetails}    {setter}
"""
    suffixFile = "Dpi.py"

    def __init__(self, data):
        super().__init__(data)
        self.dictData["isHeadLine"] = self.__getHeadLine()
        self.dictData["isMnemoCode"] = self.__getMnemoCode()
        self.dictData["deleteDetails"] = self.__getDelete()
        self.dictData["setter"] = self.__getSetter()

    def _createFile(self, path):
        # Формируем код в два прохода: сначала подставляем блоки шаблона, кроме
        # полей датакласса; затем — строки полей. Так {rop.xxx} из f-строк
        # заголовков не схлопываются format'ом и не конфликтуют с пустым attr=[].
        from core.package.FileManager import FileManagerPkg

        stage1 = self.temp.format(
            name=self.data.name,
            setter=self.dictData["setter"],
            headLine="{headLine}",
            mnemoCode="{mnemoCode}",
            attrLines="{attrLines}",
            deleteDetails=self.dictData["deleteDetails"],
            imports=self.__getImports(),
            attrForHL='\', \''.join(attr.name for attr in self.data.attr if attr.isHeadLine),
            attrForMC='\', \''.join(attr.name for attr in self.data.attr if attr.isMnemoCode)
        )
        code = (
            stage1.replace("{headLine}", self.dictData["isHeadLine"])
            .replace("{mnemoCode}", self.dictData["isMnemoCode"])
            .replace("{attrLines}", self.__getAttrLines())
        )
        FileManagerPkg.CreateFile(path, code)

    def __getAttrLines(self) -> str:
        """Строки полей датакласса: `id` обязателен, остальные — Optional со default.

        При attr=[] возвращаем только строку id: `{attrLines}` стоит в начало
        строки шаблона, лишний перевод строки дал бы мусорное поле/отступ.
        """
        lines = ["    id:int"]
        for i in self.data.attr:
            if i.name == "id":
                continue  # id всегда объявлен первым обязательным полем шаблона
            typeAttr = (
                "int"
                if i.name.startswith(("id", "n", "b"))
                else "str"
            )
            lines.append(f"    {i.name}:Optional[{typeAttr}] = None")
        return "\n".join(lines)

    def __getImports(self) -> str:
        """Дополнительные импорты в шапку файла (для каскада коллекций)."""
        return "".join(
            f"from module.{self.__getModule(collection.name)} import {collection.name}Logic\n"
            for collection in self.data.collections
        )

    @staticmethod
    def __getModule(nameClass: str) -> str:
        """Модуль класса: реестр sc (Sc_ClsLogic), фолбэк — соглашение имён."""
        from core.sdk import Sc_ClsLogic

        return Sc_ClsLogic().getPrefixModule(nameClass)

    def __getHeadLine(self):
        attrByHL = []
        for attr in self.data.attr:
            if attr.isHeadLine:
                attrByHL.append(f"rop.{attr.name}")
        return "{" + ("} {".join(attrByHL) if attrByHL != [] else "rop.id") + "}"

    def __getMnemoCode(self):
        attrByMC = []
        for attr in self.data.attr:
            if attr.isMnemoCode:
                attrByMC.append(f"rop.{attr.name}")
        return "{" + ("} {".join(attrByMC) if attrByMC != [] else "rop.id") + "}"

    def __getDelete(self) -> str:
        """Каскадное удаление дочерних записей (collections).

        Переопределение delete() внутри класса Dpi: сначала зависимые записи
        коллекций, затем сам объект (super().delete). Импорт чужих Logic — в
        шапку файла (__getImports). Без коллекций — пустая строка, чтобы блок
        не ломал отступы шаблона.
        """
        if not self.data.collections:
            return ""

        body = [
            "    def delete(self, obj):",
            "        # Каскад: сначала зависимые записи коллекций, затем сам объект",
        ]
        for collection in self.data.collections:
            logicName = f"{collection.name}Logic"
            attrObj = "id" if collection.attr.startswith("id") else "gid"
            body.append(
                f"        for i in {logicName}().getAllByAttr('{collection.attr}', obj.{attrObj}) or []:"
            )
            body.append(f"            {logicName}().delete(i)")
        body.append("        return super().delete(obj)")

        return "\n".join(body) + "\n\n"

    def __getSetter(self):
        tempSet = (
            "def set{nameAttr}(self, obj:{nameClass}Obj, value): obj.{nameAttr} = value; self.after_setter(obj, \'{nameAttr}\')"
        )
        listTepmSet = tuple(
            tempSet.format(nameAttr=i.name, nameClass=self.data.name)
            for i in self.data.attr
        )
        return "\n    ".join(listTepmSet)
