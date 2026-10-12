"""Декораторы @Oper/@Setter и реестр OperRegistry."""

from core.decorator import Oper, Setter, TypeDecorator
from core.fabric.OperRegistry import OperRegistry


class DemoPub:
    def __init__(self):
        self.calls = []

    @Oper(label="Открыть", order=20, icon="open.png", shortcut="Ctrl+O")
    def open_file(self):
        self.calls.append("open_file")

    @Oper(order=10)  # label не задан -> выводится из имени
    def new_item(self):
        pass

    @Oper(label="Удалить", order=30, headOper="menu_edit", isVisible=False)
    def delete_item(self):
        pass

    @Oper(label="Справка", order=5, headOper="menu_help", isCheckable=True)
    def help(self):
        pass

    @Setter
    def set_name(self, obj, value):
        pass

    def plain_method(self):
        pass


def _registry():
    reg = OperRegistry(DemoPub())
    reg.oper()
    reg.setter()
    return reg


class TestOperDecorator:
    def test_attributes_set(self):
        assert DemoPub.open_file._type == TypeDecorator.Oper
        assert DemoPub.open_file._id == "open_file"
        assert DemoPub.open_file._oper_label == "Открыть"
        assert DemoPub.open_file._icon_path == "open.png"
        assert DemoPub.open_file._shortcut == "Ctrl+O"

    def test_default_label_from_method_name(self):
        # имя метода с подчёркиваниями -> Title case
        assert DemoPub.new_item._oper_label == "New Item"

    def test_decorator_returns_same_function(self):
        # обёртки нет — метод остаётся вызываемым
        demo = DemoPub()
        demo.open_file()
        assert demo.calls == ["open_file"]

    def test_setter_attributes(self):
        assert DemoPub.set_name._type == TypeDecorator.Setter
        assert DemoPub.set_name._id == "set_name"


class TestOperRegistry:
    def test_only_oper_collected_and_sorted_by_order(self):
        ops = _registry().get_oper()
        ids = [op["id"] for op in ops]
        assert ids == ["help", "new_item", "open_file", "delete_item"]

    def test_plain_and_setter_methods_not_in_oper(self):
        ids = {op["id"] for op in _registry().get_oper()}
        assert "plain_method" not in ids
        assert "set_name" not in ids

    def test_fields_mapping(self):
        op = next(o for o in _registry().get_oper() if o["id"] == "delete_item")
        assert op == {
            "id": "delete_item",
            "label": "Удалить",
            "order": 30,
            "headOper": "menu_edit",
            "isVisible": False,
            "icon": None,
            "shortcut": None,
            "checkable": False,
            "tooltip": None,
        }

    def test_get_children_oper_roots_only(self):
        """Корни — это видимые операции с headOper == None (в т.ч. isVisible=False не проходят)."""
        reg = _registry()
        roots = [op["id"] for op in reg.get_children_oper()]
        assert roots == ["new_item", "open_file"]  # help/delete_item имеют headOper

    def test_invisible_operations_filtered_from_children(self):
        reg = _registry()
        # delete_item: headOper="menu_edit", но isVisible=False -> не возвращается
        assert reg.get_children_oper("menu_edit") == []

    def test_get_children_by_parent(self):
        reg = _registry()
        children = reg.get_children_oper("menu_help")
        assert [op["id"] for op in children] == ["help"]
        assert children[0]["checkable"] is True

    def test_hidden_child_not_returned(self):
        reg = _registry()
        assert reg.get_children_oper("menu_edit") == []

    def test_setter_registry(self):
        assert _registry().get_setter() == [{"id": "set_name"}]

    def test_oper_is_idempotent(self):
        reg = _registry()
        reg.oper()
        assert len(reg.get_oper()) == 4  # без дублей при повторном вызове
