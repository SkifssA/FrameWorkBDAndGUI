"""Ленивый дескриптор LazyVal."""

import pytest

from core.package.LazyVal import LazyVal


class TestLazyVal:
    def test_computed_once_on_descriptor_access(self):
        calls = []

        def factory():
            calls.append(1)
            return "value"

        class A:
            val = LazyVal(factory)

        assert A.val == "value"
        assert A().val == "value"
        assert len(calls) == 1  # ленивость: значение вычисляется один раз

    def test_attr_arguments_passed_to_factory(self):
        def add(a, b):
            return a + b

        lazy = LazyVal(add, attr=(2, 3))
        assert lazy._get_value() == 5

    def test_proxy_getattr_forwards_to_value(self):
        lazy = LazyVal(lambda: {"k": 1})
        assert lazy.get("k") == 1

    def test_dunder_names_raise_attributeerror(self):
        """Dunder-имена не проксируются (защита от копирования/питона-магии)."""
        lazy = LazyVal(lambda: "s")
        with pytest.raises(AttributeError):
            lazy.__deepcopy__

    def test_not_evaluated_before_access(self):
        calls = []

        class A:
            val = LazyVal(lambda: calls.append(1) or 42)

        _ = A()  # создание экземпляра не должно запускать вычисление
        assert calls == []
        assert A.val == 42
        assert calls == [1]
