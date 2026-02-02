import threading
import time
import asyncio
import datetime

from core.package import Core_ActionDispatcher
from .scriptscheduler.Bc_ScriptSchedulerApi import Bc_ScriptSchedulerObj, Bc_ScriptSchedulerApi
from .timeline.Bc_TimeLineApi import Bc_TimeLineApi

class Bc_ScriptSchedulerPkg:
    nHour = -1
    nMinute = -1
    nSec = -1
    script = {
        'hour': {}
        ,'minute' : {}
        ,'sec': {}    
    }

    @classmethod
    async def run(cls):
        await Bc_TimeLineApi().fill()
        data = await Bc_ScriptSchedulerApi()._getAllByAttr('bUsed', 1) or []
        obj = Bc_ScriptSchedulerPkg(data)
        print(obj.script)
        threading.Thread(target=obj._run).start()

    def __init__(self, objScript:tuple[Bc_ScriptSchedulerObj]):
        for obj in objScript:
            if obj.idTimeLine == Bc_TimeLineApi.idHour:
                self.fillDict(obj, 'hour')
            elif obj.idTimeLine == Bc_TimeLineApi.idMinute:
                self.fillDict(obj, 'minute')
            elif obj.idTimeLine == Bc_TimeLineApi.idSecond:
                self.fillDict(obj, 'sec')
        
    def fillDict(self, obj:Bc_ScriptSchedulerObj, TimeLine):
        for i in obj.nTime.split(','):
            if Bc_ScriptSchedulerPkg.script[TimeLine].get(i, None) is None:
                Bc_ScriptSchedulerPkg.script[TimeLine][i] = []

            Bc_ScriptSchedulerPkg.script[TimeLine][i].append(obj.sNameScript)


    def _run(self):
        while True:
            t = datetime.datetime.now()
            if self.nSec != t.second:
                self.nSec = t.second
                self._runByTime("sec", self.nSec)

            if self.nMinute != t.minute:
                self.nMinute = t.minute
                self._runByTime("minute", self.nMinute)

            if self.nHour != t.hour:
                self.nHour = t.hour
                self._runByTime("hour", self.nHour)

            time.sleep(0.50)

    def _runByTime(self, TimeLine, Time):
        
        def k(name):
            asyncio.run(Core_ActionDispatcher().action(name))

        for i in Bc_ScriptSchedulerPkg.script[TimeLine].get(str(Time), []):
            threading.Thread(target=k, args=(i, )).start()


