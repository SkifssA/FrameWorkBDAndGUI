from engine.package import ASQL, ActionDispatcher

class ScriptManager:
    async def execute_pending(self, datas: list[dict]):
        for data in datas:
            if await self._needs_update(data):
                await self._resolve_deps(data, datas)
                await ActionDispatcher().action(data["name"])
                await self._update_db_state(data)

    async def _resolve_deps(self, data: dict, all_datas: list[dict]):
        deps = data.get("dependence")
        if not deps: return
        dep_list = [deps] if isinstance(deps, str) else deps
        for dep_name in dep_list:
            dep_data = next((d for d in all_datas if d.get("name") == dep_name), None)
            if dep_data: await self.execute_pending([dep_data])

    async def _needs_update(self, data: dict) -> bool:
        res = await ASQL("SELECT nVersion FROM Script WHERE sAction = ?", (data["name"],))
        return not res or res[0]["nVersion"] < data["version"]

    async def _update_db_state(self, data: dict):
        exists = await ASQL("SELECT 1 FROM Script WHERE sAction = ?", (data["name"],))
        query = ("INSERT INTO Script (nVersion, sAction) VALUES (?, ?)" 
                 if not exists else 
                 "UPDATE Script SET nVersion = ? WHERE sAction = ?")
        await ASQL(query, (data["version"], data["name"]))  # ← поправил ATQSL → ASQL


ScriptsManager = ScriptManager()