from textual.app import App, Screen
from textual.widgets import Button
from textual.containers import VerticalScroll, Horizontal

from ..package import Core_FileManagerPkg, ATQSL
from ..widgets import ButtonApp, DefaultLookUp

class Core_MainMenu(Screen):
    CSS="""
    #toolbar {
        width: 100%;
        height: auto;
    }
    LookUp {
        width: auto;
        height: auto;
    }
    """
    def compose(self):
        yield Horizontal(
            id = 'toolbar'
        )
        yield VerticalScroll(id="app_containers")

    async def on_mount(self):
        await self.onRefresh()

    async def onRefresh(self):
        containers = self.query_one("#app_containers", VerticalScroll)
        containers.remove_children()
        listApp = await Core_FileManagerPkg.ReadFile("../../project.yaml")
        for app in listApp['modules']:
            if await Core_FileManagerPkg.Exists(f"../../{app}/config/configApp.json"):
                data = await Core_FileManagerPkg.ReadFile(f"../../{app}/config/configApp.json")
                containers.mount(ButtonApp(app, data))