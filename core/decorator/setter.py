SETTER = "setter"


def Setter(func):
    """Декоратор для методов-сеттеров"""
    func._type = SETTER
    func._id = func.__name__
    return func
