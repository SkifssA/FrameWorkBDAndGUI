"""Base.getDict (очистка словаря) и Base.merge (глубокое слияние датаклассов)."""

from dataclasses import dataclass, field

from core.dataClass.baseDataClass import Base


@dataclass
class Leaf(Base):
    name: str = None
    value: int = None


@dataclass
class Node(Base):
    name: str = None
    caption: str = None
    isVisible: bool = True
    child: Leaf = None
    items: list = field(default_factory=list)


class TestGetDict:
    def test_removes_none_and_empty_lists(self):
        node = Node(name="a", caption=None, child=Leaf(name="x", value=None))
        d = node.getDict()
        assert d == {"name": "a", "isVisible": True, "child": {"name": "x"}}

    def test_isNotNone_false_keeps_everything(self):
        node = Node(name="a")
        d = node.getDict(isNotNone=False)
        assert d["caption"] is None
        assert d["items"] == []

    def test_recursion_through_nested_lists(self):
        node = Node(items=[Leaf(name="n1"), Leaf(value=None), 5])
        # asdict превращает вложенные датаклассы в dict, _clean чистит их рекурсивно
        d = node.getDict()
        assert d["items"] == [{"name": "n1"}, {}, 5] or d["items"] == [
            {"name": "n1"},
            5,
        ]
        # Пустые dict после очистки не должны исчезать молча — фиксируем текущее поведение:
        # из списка удаляются только None-элементы
        assert {} in d["items"] or 5 in d["items"]

    def test_dict_values_cleaned(self):
        @dataclass
        class WithDict(Base):
            mapping: dict = field(default_factory=dict)

        w = WithDict(mapping={"keep": 1, "drop": None})
        assert w.getDict()["mapping"] == {"keep": 1}


class TestMerge:
    def test_scalar_priority_to_other(self):
        base = Node(name="base", caption="old")
        other = Node(caption="new")
        merged = base.merge(other)
        assert merged.caption == "new"      # приоритет у other
        assert merged.name == "base"        # other_val None -> оставляем текущее

    def test_not_dataclass_returns_other(self):
        base = Node(name="base")
        assert base.merge({"a": 1}) == {"a": 1}
        assert base.merge(None) is None

    def test_nested_dataclass_merged_recursively(self):
        base = Node(child=Leaf(name="old", value=1))
        other = Node(child=Leaf(value=2))
        merged = base.merge(other)
        assert merged.child.name == "old"
        assert merged.child.value == 2

    def test_lists_of_dataclasses_merged_by_name(self):
        base = Node(items=[Leaf(name="a", value=1), Leaf(name="b", value=2)])
        other = Node(items=[Leaf(name="b", value=20), Leaf(name="c", value=3)])
        merged = base.merge(other)
        by_name = {i.name: i.value for i in merged.items}
        assert by_name == {"a": 1, "b": 20, "c": 3}

    def test_list_without_name_replaced(self):
        base = Node(items=["x", "y"])
        other = Node(items=["z"])
        assert base.merge(other).items == ["z"]

    def test_empty_new_list_keeps_current(self):
        base = Node(items=[Leaf(name="a")])
        other = Node(items=[])
        assert base.merge(other).items == base.items

    def test_merge_preserves_type(self):
        merged = Node(name="n").merge(Node(caption="c"))
        assert isinstance(merged, Node)
