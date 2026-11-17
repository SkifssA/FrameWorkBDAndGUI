def build_columns_from_meta(meta_form: dict) -> list[dict]:
    """
    Преобразует metaForm.attr в колонки Tabulator
    """
    columns = []
    
    # Сортируем по order
    attrs = sorted(meta_form["attr"], key=lambda x: x.get("order", 0))
    
    for attr in attrs:
        # Пропускаем невидимые поля
        if not attr.get("isVisible", True):
            continue
        
        col = {
            "title": attr["caption"],
            "field": attr["name"],
        }
        
        # Настройка по типу
        attr_type = attr.get("type", "TEXT")
        edit_type = attr.get("editType", "edit")
        
        # Чекбоксы
        if edit_type == "check":
            col["formatter"] = "tickCross"
            col["hozAlign"] = "center"
        
        # Числа
        elif attr_type == "INT":
            col["hozAlign"] = "right"
        
        # Текст
        elif attr_type == "TEXT":
            pass
        # Lookup (пока показываем ID, потом заменим на связанное значение)
        elif edit_type == "lookUp":
            pass
            # Можно добавить кастомный formatter для отображения названия
        
        columns.append(col)
    
    return columns


def build_table_config_from_meta(meta_form: dict) -> dict:
    """
    Строит полный конфиг для Tabulator из метаданных
    """
    return {
        "columns": build_columns_from_meta(meta_form['metaForm']),
        "url": f"/api/{meta_form['metaForm']['name']}/rows",
        "options": {
            "movableColumns": True,
            "resizableColumns": True,
        }
    }