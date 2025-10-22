class Oper:
    def __init__(self, scen, op:str|list[str]):
        if isinstance(op, str):
            ops = [op]
        elif isinstance(op, list):
            ops = op
        else:
            raise TypeError("op должен быть str или list[str]")
        self.oper = []
        for i in ops:
            self.oper.append(scen.query_one(f'#{i}'))

    @property
    def isDisabled(self) -> bool:
        pass

    @isDisabled.setter
    def isDisabled(self, value):
        for i in self.oper:
            i.disabled = value