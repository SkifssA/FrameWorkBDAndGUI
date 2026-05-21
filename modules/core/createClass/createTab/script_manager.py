from engine.package import ActionDispatcher

from modules.core.createClass.createTab.class_for_tab import dbData

from modules.core.object.script.Core_ScriptApi import Core_ScriptApi

class ScriptManager:
    async def execute_pending(self, datas: list[dbData]):
        for data in datas:
            if await self._needs_update(data):
                await self._resolve_deps(data, datas)
                ActionDispatcher().action(data.name)
                await self._update_db_state(data)

    async def _resolve_deps(self, data: dbData, all_datas: list[dbData]):
        deps = data.dependence
        if not deps: return
        dep_list = [deps] if isinstance(deps, str) else deps
        for dep_name in dep_list:
            dep_data = next((d for d in all_datas if d.name == dep_name), None)
            if dep_data: await self.execute_pending([dep_data])

    async def _needs_update(self, data: dbData) -> bool:
        objScript = Core_ScriptApi().getByMnemocode(data.name)
        return not objScript or objScript.nVersion < data.version

    async def _update_db_state(self, data: dbData):
        if ropScript:=Core_ScriptApi().getByMnemocode(data.name):
            ropScript.nVersion = data.version
        else:
            ropScript = Core_ScriptApi().insert()
            ropScript.sCode = data.name
            ropScript.nVersion = data.version
        Core_ScriptApi().update(ropScript)


ScriptsManager = ScriptManager()