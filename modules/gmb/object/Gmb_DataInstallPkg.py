from modules.bc import Bc_ConfigApi, Bc_ScriptSchedulerApi, Bc_TimeLineApi

class Gmb_DataInstallPkg:
    async def dataInstallConfig(self):
        await Bc_ConfigApi().registerByModule('gmb', 'baseUrlGitLab', 'https://extgit.global-system.ru')
        await Bc_ConfigApi().registerByModule('gmb', 'privateTokenGitLab', 'glpat-DnMzYcvuc7Wizzhxqo8y')

        await Bc_ConfigApi().registerByModule('gmb', 'modulesRootPath', 'C:\\programs\\gsf-cli\\workspace\\sources\\pgDev\\application')
        await Bc_ConfigApi().registerByModule('gmb', 'beginHourWork', '9')
        await Bc_ConfigApi().registerByModule('gmb', 'endHourWork', '18')

        Bc_ScriptSchedulerApi().register('Gmb_GitLabManagerPkg.MRMonitor', nTime=30, idTimeLine=Bc_TimeLineApi.idSecond)

