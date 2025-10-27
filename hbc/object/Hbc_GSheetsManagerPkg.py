import pandas as pd
import asyncio

from bc.object.config.Bs_ConfigApi import Bs_ConfigApi
from ..object import Hbc_StudentApi, Hbc_StudentDataApi



class Hbc_GSheetsManagerPkg:
    _url = 'https://docs.google.com/spreadsheets/d/{0}/export?format=csv&gid={1}'

    async def GetStudents(self):
        # Используем pandas для обработки
        idGS = await Bs_ConfigApi().getValueByModule('hbc', 'idGSheets')
        idMainList = await Bs_ConfigApi().getValueByModule('hbc', 'idMainListGSheets')
        nameCurator = await Bs_ConfigApi().getValueByModule('hbc', 'firstNameLastName')
        df = await asyncio.to_thread(pd.read_csv, self._url.format(idGS, idMainList))
        filtered_df = df[df['Куратор'] == nameCurator].to_dict()  # Замените 'Столбец' на нужное имя
        for idS in filtered_df['Unnamed: 0'].keys():
            id = await Hbc_StudentApi().register(filtered_df['Unnamed: 0'][idS]
                                            ,filtered_df['Контакт'][idS]
                                            ,filtered_df['Виртуалка'][idS]
                                            ,filtered_df['Unnamed: 11'][idS]
                                            ,filtered_df['Unnamed: 12'][idS]
                                        )
            await Hbc_StudentDataApi().register(id, filtered_df['Дата выхода'][idS])