class SQLBuild:
    def __init__(self, sTablet:str, alias='t'):
        self._select = []
        self._join = []
        self._scalar = []
        self._where = []
        self._group_by = []
        self._order_by = []

    def select(self, listSelect: list[str])->'SQLBuild':
        self._select.extend(listSelect)
        return self

    def join(self, joinTab:str, on:str, alias:str, isLeft:bool=False)->'SQLBuild':
        self._join.append(f'{'LEFT' if isLeft else ''} JOIN {joinTab} {alias} on {on}')
        return self

    def scalar(self, listSelect: list[str])->'SQLBuild':
        self._select.extend(listSelect)
        return self

    def build()->str:
        pass

    def buildExt()->str:
        pass