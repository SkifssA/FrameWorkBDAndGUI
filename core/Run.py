import flet as ft

from core.Core_SelectApp import Core_SelectApp
from core.Core_Store import store

async def mainProgram(page: ft.Page):
    page.title = "Мульти-страничное приложение"
    store.page = page
    await Core_SelectApp().open()