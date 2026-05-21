from modules.bc import Bc_ScriptSchedulerApi
from modules.bc.object.timeline.Bc_TimeLineApi import Bc_TimeLineApi

class Awh_DataInstallPkg:
    async def dataInstallScript(self):
        Bc_ScriptSchedulerApi().register('Awh_AnimeApi.updateAnime', nTime=18, idTimeLine=Bc_TimeLineApi.idHour)
