from textual.app import Screen
from textual.widgets import Static
from textual.containers import Vertical
import asyncio

from ..widgets import LoadingIndicator

class RunningScreen(Screen):
    CSS = """
    Static {
        width: 100%;
        height: auto;
        text-align: center;
    }
    #RunningVertical {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    """
    def __init__(self, task_func, on_done=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_func = task_func
        self.on_done = on_done

    def compose(self):
        with Vertical(id="RunningVertical"):
            yield LoadingIndicator()
            yield Static("🔄 Выполняется задача...", id="progress")
            yield Static("Она не зависла, честно...", id="comedian")

    async def on_mount(self):
        self.update_progress("Задача запущена...")
        # Запускаем задачу в фоне
        asyncio.create_task(self.run_task())


    def update_progress(self, msg):
        try:
            self.query_one("#progress", Static).update(msg)
        except Exception as e:
            self.log(f"Ошибка обновления: {e}")

    async def run_task(self):
        # Выполняем задачу в фоне
        try:
            await self.task_func(self.update_progress)
        except Exception as e:
            self.update_progress(f"❌ Ошибка: {e}")
            await asyncio.sleep(2)
            self.app.pop_screen()
            return

        self.update_progress("✅ Готово!")
        if self.on_done:
            await asyncio.sleep(1)
            await self.on_done()
        await asyncio.sleep(1)
        self.app.pop_screen()