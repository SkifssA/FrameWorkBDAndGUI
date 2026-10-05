from engineQT.ui.inputs.base import Base

class SetterEvent:
    def __init__(self, editor:Base):
        data = editor.getValue()
        self.value = data['value']
        self.user_data = data.get('user_data')