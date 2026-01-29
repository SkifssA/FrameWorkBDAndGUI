from modules.bc import Bc_ScriptSchedulerApi

class Awh_DataInstallPkg:
    async def dataInstallScript(self):
        await Bc_ScriptSchedulerApi().register('Awh_AnimeApi.updateAnime', sSec='30')
