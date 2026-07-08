from modules.bc.object.config.Bc_ConfigApi import Bc_ConfigApi

class Hbc_DataInstallPkg:
    async def dataInstallConfig(self):
        await Bc_ConfigApi().registerByModule('hbc', 'loginNewProfi', 'a.kopylov')
        await Bc_ConfigApi().registerByModule('hbc', 'passwordNewProfi', 'wW8iK3lY')

        await Bc_ConfigApi().registerByModule('hbc', 'idGSheets', '1sb70FeN6MKImV7XqLP2Vkan-56Hg_4OLnZMjBIcJRcE')
        await Bc_ConfigApi().registerByModule('hbc', 'idMainListGSheets', '2128669617')
        await Bc_ConfigApi().registerByModule('hbc', 'idSubListGSheets', '0')
