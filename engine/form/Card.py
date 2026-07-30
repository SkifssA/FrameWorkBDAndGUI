import dearpygui.dearpygui as dpg
import time
import re

from engine.package import ASQL
from engine.form.Base import Base
from engine.package.ThreadWorkerPkg import tw

from engine.form.widgets.input.base import Base as baseInput
from engine.form.widgets.input.multiText import multiText
from engine.form.widgets.input.check import Check
from engine.form.widgets.input.lookUp import LookUp
from engine.form.widgets.input.button import ButtonRef

class Card(Base):
    inputClass:dict[str, baseInput] = {
        'multiText':multiText
        ,'edit':baseInput
        ,'check':Check
        ,'lookUp':LookUp
        ,'button':ButtonRef
    }

    def __init__(self):
        super().__init__()
        self.tagInput = {}
        self.input:dict[str, Base] = {}
        self.obj = None
        self.sizeButton = 30

    def createMainForm(self, par):
        self.sizeBefore = 100
        with dpg.child_window(parent=par) as group:
            w = dpg.add_group()
            backLastLine = True
            row = [[]]
            for i in sorted(self.meta['attr'], key=lambda x: self.meta['attr'][x]['order']):
                self.createGroupInput(i, w, backLastLine)
        
        row = row[:-1]
        
        # === ИСПРАВЛЕНИЕ ===
        # 1. Создаем реестр обработчиков
        with dpg.item_handler_registry() as registry:
            # 2. Добавляем обработчик изменения размера
            # Передаем registry в user_data, чтобы потом удалить его
            dpg.add_item_resize_handler(
                callback=self._on_form_ready, 
                user_data=(row, group, registry)
            )
        
        # 3. Привязываем реестр к нашему child_window (group)
        dpg.bind_item_handler_registry(group, registry)
        
        return group

    def _on_form_ready(self, sender, app_data, user_data):
        """
        Этот метод автоматически вызовется в главном потоке GUI, 
        как только DPG рассчитает размеры child_window.
        """
        row, mainForm, registry_tag = user_data
        
        if dpg.does_item_exist(mainForm):
            size = dpg.get_item_rect_size(mainForm)
            # Проверяем, что форма реально отрисована и имеет ширину > 0
            if size[0] > 0:
                # Выполняем ваши расчеты
                self.w(row)
                self.MaxHeightTitle(row)

    def w(self, rows):
        for row in rows:
            if row != []:
                r = len(row)
                q = dpg.get_item_rect_size(self.mainForm)[0] - 20 - 8*(r-1)
                s = q // r
                maxW = q - s * r
                for j in row:
                    p = dpg.get_item_parent(j)
                    nChild = len(dpg.get_item_children(j)[1])
                    if nChild > 2:
                        w = dpg.get_item_children(j)[1]
                        dpg.set_item_width(w[1], s - ((self.sizeButton + 40) * 3 + 10))
                    dpg.set_item_width(p, s + maxW if j == row[-1] else s)
    
    def MaxHeightTitle(self, row):
        w = 0
        r = [i[0] for i in row if i != []]
        cw = []
        for i in r:
            p = dpg.get_item_parent(i)
            cw.append(dpg.get_item_children(p)[1][0])
            l = dpg.get_item_children(cw[-1])[1][0]
            value = dpg.get_value(l) or ''
            if w < len(value):
                w = len(value)
        sizeLable = w * 11
        for i in cw:
            dpg.set_item_width(i, sizeLable)
        
    def createGroupInput(self, nameAttr:str, groupParent, selfSizeName=False):
        dataAttr = self.meta['attr'][nameAttr]
        data = {
            'classCard': self
            ,'nameAttr': nameAttr
            ,'parent': groupParent
        }
        self.input[nameAttr] = Card.inputClass.get(dataAttr['edit'], lambda **x: print("ТАКОГО ТИПА РЕДОКТРОВАНИЯ НЕТ"))(**data)

    async def initInput(self):
        if obj:=self.thisRop():
            dpg.configure_item(self.tab, label=self.thisApi().calcHeadLine(obj))
        for key, value in self.rect.getData()[0].items():
            if key in self.input.keys():
                self.input[key].init(value)

    async def _refresh(self):
        self.rect.refresh()
        await self.initInput()
        self.checwork()

    def afterSetter(self):
        self.isMod = True
        self.checwork()

    def _getAttr(self, nameAttr:str):
        return self.input[nameAttr].value   