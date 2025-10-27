from bc.object.config.Bs_ConfigApi import Bs_ConfigApi

class Hbc_DataInstallPkg:
    async def dataInstallConfig(self):
        await Bs_ConfigApi().insertByModule('hbc', 'loginNewProfi', 'a.kopylov')
        await Bs_ConfigApi().insertByModule('hbc', 'passwordNewProfi', 'wW8iK3lY')

        await Bs_ConfigApi().insertByModule('hbc', 'idGSheets', '1sb70FeN6MKImV7XqLP2Vkan-56Hg_4OLnZMjBIcJRcE')
        await Bs_ConfigApi().insertByModule('hbc', 'idMainListGSheets', '2128669617')
        await Bs_ConfigApi().insertByModule('hbc', 'idSubListGSheets', '0')
