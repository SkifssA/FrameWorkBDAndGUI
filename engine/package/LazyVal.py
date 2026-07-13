class LazyVal:
    """Дескриптор для ленивого вычисления ID по мнемонике."""
    def __init__(self, func):
        self.func = func
        self._value = None
        self._computed = False

    def _get_value(self):
        if not self._computed:
            self._value = self.func()
            self._computed = True
        return self._value

    # def __get__(self, instance, owner):
    #     # Для использования как дескриптора класса
    #     return self._get_value()

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(name)
        # Проксирует вызовы к вычисленному значению (для модульного уровня)
        return getattr(self._get_value(), name)