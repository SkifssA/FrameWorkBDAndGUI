from dataclasses import dataclass, field
from dacite import from_dict, Config

from core.DB import ASQL
from core.dataClass.baseDataClass import Base

BASE_ATTR = [
    {
        "name": "id",
        "caption": "id",
        "type": "INT",
        "edit": "edit",
        "isVisible": False,
        "order": -2,
    },
    {
        "name": "gid",
        "caption": "gid",
        "type": "TEXT",
        "edit": "edit",
        "isVisible": False,
        "order": -1,
    }
]

TYPE_MAPPING: dict[str, str] = {
    "TEXT": "TEXT",
    "STRING": "TEXT",
    "INT": "INTEGER",
    "INTEGER": "INTEGER",
    "LONG": "INTEGER",
    "BOOLEAN": "INTEGER",
    "DATE": "TEXT",
}

SERVICE_COLUMNS = ("id", "sHeadLine", "sMnemoCode", "gid")


@dataclass
class collectionsSchema(Base):
    name: str
    attr: str


@dataclass
class attrSchema(Base):
    name: str
    caption: str
    type: str
    isHeadLine: bool = False
    isMnemoCode: bool = False
    isVisible: bool = True
    order: int = 0
    editType: str = "edit"
    display: str = None
    refTab: str = None

    def getSql(self) -> str:
        """SQL-объявление колонки таблицы."""
        return f"{self.name} {TYPE_MAPPING.get(self.type, 'TEXT')}"


@dataclass
class dbDataSchema(Base):
    """Скрипт установки/накатки данных таблицы (*.odb.json -> dbData)."""

    name: str
    version: int = None
    dependence: str | list = None


@dataclass
class tabSchema(Base):
    name: str
    caption: str
    collections: list[collectionsSchema] = field(default_factory=list)
    attr: list[attrSchema] = field(default_factory=list)
    dbData: list[dbDataSchema] = field(default_factory=list)
    # служебные поля миграции (не из json)
    isNew: bool = False
    minListAttr: list[str] = field(default_factory=list)

    def getSQL(self) -> str:
        """DDL таблицы: служебные колонки + колонки из attr."""
        columns = ",\n    ".join(attr.getSql() for attr in self.attr)
        return f"""
    CREATE TABLE {self.name}{"_new" if self.isNew else ""} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sHeadLine TEXT,
        sMnemoCode TEXT UNIQUE,
        gid TEXT UNIQUE,
        {columns}
    )
    """

    def execute_pending(self):
        """Создать таблицу; если это миграция (isNew) — перенести данные и переименовать."""
        ASQL(self.getSQL())
        if self.isNew:
            sListAttr = ", ".join(self.minListAttr)
            ASQL(f"""
                INSERT INTO {self.name}_new({sListAttr})
                SELECT {sListAttr} FROM {self.name};
            """)
            ASQL(f"""DROP TABLE {self.name};""")
            ASQL(f"""ALTER TABLE {self.name}_new RENAME TO {self.name};""")
