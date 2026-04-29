
class SetterEvent:
    def __init__(self, class_, type=None):
        self.value = None
        self.user_data = None
        self.sender = None
        self.type = type
        self.class_ = class_

    def get(self, sAttr):
        getattr(self.class_, f'set{sAttr}', None)(self)

    def getEvent(self, sAttr):
        def fillEvent(sender, value, user_data):
            self.value = value
            self.sender = sender
            self.user_data = user_data
            self.get(sAttr)
        return fillEvent