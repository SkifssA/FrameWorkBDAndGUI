import threading
import time
import datetime

from engine.package import ActionDispatcher, tw
from modules.bc.object.scriptscheduler.Bc_ScriptSchedulerApi import Bc_ScriptSchedulerObj, Bc_ScriptSchedulerApi
from modules.bc.object.timeline.Bc_TimeLineApi import Bc_TimeLineApi

class Bc_ScriptSchedulerPkg:
    nHour = -1
    nMinute = -1
    nSec = -1
    runMe = False
    script = {
        'hour': {}
        ,'minute' : {}
        ,'sec': {}    
    }

    @classmethod
    async def run(cls):
        data = Bc_ScriptSchedulerApi()._getAllByAttr('bUsed', 1)
        obj = Bc_ScriptSchedulerPkg(data)
        obj.runMe = True
        tw.submit(obj._run)
        return obj

    def __init__(self, objScript:tuple[Bc_ScriptSchedulerObj]):
        self.fillDict(objScript=objScript)
        
    def fillDict(self, objScript):
        self.script = {
            'hour': {}
            ,'minute' : {}
            ,'sec': {}    
        }
        for obj in objScript:
            if obj.idTimeLine == Bc_TimeLineApi.idHour:
                self._fillDict(obj, 'hour')
            elif obj.idTimeLine == Bc_TimeLineApi.idMinute:
                self._fillDict(obj, 'minute')
            elif obj.idTimeLine == Bc_TimeLineApi.idSecond:
                self._fillDict(obj, 'sec')

    def _fillDict(self, obj:Bc_ScriptSchedulerObj, TimeLine):
        for i in str(obj.nTime).replace(' ', '').split(','):
            if Bc_ScriptSchedulerPkg.script[TimeLine].get(i, None) is None:
                Bc_ScriptSchedulerPkg.script[TimeLine][i] = []

            Bc_ScriptSchedulerPkg.script[TimeLine][i].append(obj.sNameScript)


    def _run(self):
        while self.runMe:
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
            ActionDispatcher().action(name)

        for i in Bc_ScriptSchedulerPkg.script[TimeLine].get(str(Time), []):
            threading.Thread(target=k, args=(i, ), daemon=True).start()


