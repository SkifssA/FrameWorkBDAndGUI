from core.DB.Turso import ASQL

from core.package import asyncRun

TYPE_MAPPING: dict[str, str] = {
    "TEXT": "TEXT"
    , "STRING": "TEXT"
    , "INT": "INTEGER"
    , "INTEGER": "INTEGER"
    , "LONG": "INTEGER"
    , "BOOLEAN": "INTEGER"
    , "DATE": "TEXT"
}

class Tab:
    def __init__(self, **arg):
        self.name = arg.get('name', None)
        self.caption = arg.get('caption', self.name)
        self._isNew = False

        self.attr:list[Attr] = []
        if 'attr' in arg:
            for i in arg['attr']:
                self.attr.append(Attr(**i))

        self.coll:list[Coll] = []
        if 'coll' in arg:
            for i in arg['coll']:
                self.coll.append(Coll(**i))

        self.dbData:list[dbData] = []
        if 'dbData' in arg:
            for i in arg['dbData']:
                self.dbData.append(dbData(**i))

    def isNew(self, minListAttr):
        self._isNew = True
        self.minListAttr = minListAttr

    def getSQL(self):
        return f"""
CREATE TABLE {self.name}{'_new' if self._isNew else ''} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gid TEXT,
    sHeadLine TEXT,
    sMnemoCode TEXT UNIQUE,
    {',\n    '.join(attr.getSql() for attr in self.attr)}
)
"""
    
    def execute_pending(self):
        asyncRun(ASQL(self.getSQL()))
        if self._isNew:
            sListAttr = ', '.join(self.minListAttr)
            asyncRun(ASQL(f"""
                INSERT INTO {self.name}_new({sListAttr})
                SELECT {sListAttr} FROM {self.name};
            """))
            asyncRun(ASQL(f"""DROP TABLE {self.name};"""))
            asyncRun(ASQL(f"""ALTER TABLE {self.name}_new RENAME TO {self.name};"""))

class Attr:
    def __init__(self, **arg):
        self.name = arg.get('name', None)
        self.type = arg.get('type', None)
        self.caption = arg.get('caption', self.name)
        self.isMnemoCode = arg.get('isMnemoCode', False)
        self.isHeadLine = arg.get('isHeadLine', False)
        self.isVisible = arg.get('isVisible', True)
        self.refTab = arg.get('refTab', None)

    def getSql(self):
        return f'{self.name} {TYPE_MAPPING.get(self.type, 'TEXT')}'

class Coll:
    def __init__(self, **arg):
        self.name = arg.get('name', None)
        self.attr = arg.get('attr', None)

class dbData:
    def __init__(self, **arg):
        self.name = arg.get('name', None)
        self.version = arg.get('version', None)
        self.dependence = arg.get('dependence', None)