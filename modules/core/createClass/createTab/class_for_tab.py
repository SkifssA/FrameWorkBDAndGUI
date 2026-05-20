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
        self.attr = []
        if 'attr' in arg:
            for i in arg['attr']:
                self.attr.append(Attr(**i))
        self.coll = []
        if 'coll' in arg:
            for i in arg['coll']:
                self.attr.append(Coll(**i))


class Attr:
    def __init__(self, **arg):
        self.name = arg.get('name', None)
        self.type = arg.get('type', None)
        self.caption = arg.get('caption', self.name)
        self.isMnemoCode = arg.get('isMnemoCode', False)
        self.isHeadLine = arg.get('isHeadLine', False)
        self.isVisible = arg.get('isVisible', True)
        self.refTab = arg.get('refTab', None)


class Coll:
    def __init__(self, **arg):
        self.name = arg.get('name', None)
        self.attr = arg.get('attr', None)