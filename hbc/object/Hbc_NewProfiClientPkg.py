from core.package import Core_AiohttpPkg
from ..object.lesson.Hbc_LessonApi import Hbc_LessonApi
from ..object.studentdata.Hbc_StudentDataApi import Hbc_StudentDataApi
from ..object.student.Hbc_StudentApi import Hbc_StudentApi
from ..object.studentlesson.Hbc_StudentLessonApi import Hbc_StudentLessonApi

from bc.object.config.Bc_ConfigApi import Bc_ConfigApi
from bc.object.file.Bc_FileApi import Bc_FileApi

class Hbc_NewProfiClientPkg(Core_AiohttpPkg):
    _domen = "https://newprofi-edu.ru"
    _nameCSRFToken = "logintoken"
    _url = {
        "login": "/login/index.php"
        ,"allStudent": "/blocks/completion_progress/overview.php?instanceid=256&courseid=125&page=0&perpage=0&group=0&role=13"
        ,"getAssign": "/mod/assign/view.php?id={idAssign}&action=grade&userid={idStudent}"
        ,"getQuiz": "/mod/quiz/report.php?id={idQuiz}&mode=overview&attempts=enrolled_with&onlygraded&states=finished&group=0&onlyraded=1&slotmarks=0&tifirst={firstInitial}&tilast={lastInitial}"
        ,"view": "/mod/assign/view.php{attr}"
    }

    async def _getAllStudentHtml(self):
        try:
            async with self.get('allStudent') as response:
                return await response.text()
        except Exception as e:
            print(f"Ошибка: {e}")
            return None

    async def Login(self):
        await super().Login(await Bc_ConfigApi().getValueByModule('hbc', 'loginNewProfi'), 
                            await Bc_ConfigApi().getValueByModule('hbc', 'passwordNewProfi'), 
                            withCSRFToken=True)

    async def dataInstall(self):
        await self.Login()
        content = await self._getAllStudentHtml()
        await self.fillConfigName(content)
        trs = await self.findAll(content, 'tr', attrs={'id': lambda x: x and x.startswith('block-completion_progress-overview_r')})
        await self._createDataLesson(trs[0])

    async def fillConfigName(self, text):
        userName = (await self.findAll(text, 'span', class_='usertext mr-1'))[0].get_text().strip()
        await Bs_ConfigApi().insertByModule('hbc', 'firstNameLastName', ' '.join(userName.split(' ')[:-1]))

    async def _createDataLesson(self, html):
        divs = await self.findAll(html, 'div', class_='progressEventInfo',
                            attrs={'id': lambda x: x and x.startswith('progressBarInfo') and not x.endswith('info')})
        for div in divs:
            a = div.find('a', class_='action_link')
            mod = await self._reSearch(r'/mod/([^/]+)/', a['href'])
            if mod == 'assign':
                id = await self._reSearch(r'[?&]id=(\d+)', a['href'])
                sCaption = a.get_text().strip()
                await Hbc_LessonApi().register(id, sCaption)

    async def createFileStudents(self, students: list, update_progress=None):
        content = await self._getAllStudentHtml()
        trs = await self.findAll(content, 'tr', attrs={'id': lambda x: x and x.startswith('block-completion_progress-overview_r')})
        for tr in trs:
            await self._createFileStudent(tr, students, update_progress)

    async def _createFileStudent(self, html, students, update_progress=None):
        labelUser = (await self.findAll(html, 'label', attrs={'for': lambda x: x and x.startswith('user')}))[0]
        userName = labelUser.get_text(strip=True).replace('Select', '').replace('\'', '').strip()
        if userName in students:
            print('Ученик найден')
            id = labelUser['for'].replace('user', '')
            ropStudent = await Hbc_StudentApi().getByName(userName)
            await Hbc_StudentApi().setsIdNew(ropStudent, id)
            divs = await self.findAll(html, 'div', class_='progressEventInfo',
                                      attrs={'id': lambda x: x and x.startswith('progressBarInfo')})
            for div in divs[1:]:
                state = div.find('img', class_='icon iconInInfo')['alt']
                if (state != 'Не выполнено'):
                    a = div.find('a', class_='action_link')
                    mod = await self._reSearch(r'/mod/([^/]+)/', a['href'])
                    if mod in ['assign', 'quiz']:
                        idLesson = await self._reSearch(r'[?&]id=(\d+)', a['href'])
                        if mod == 'assign':
                            ropLesson = await Hbc_LessonApi().getByIdExit(idLesson)
                            if update_progress:
                                update_progress(f'Для {Hbc_StudentApi().calcHeadLine(ropStudent)} проверяем урок {Hbc_LessonApi().calcHeadLine(ropLesson)}')
                            await Hbc_StudentLessonApi().register(ropStudent.id, ropLesson.id)
                        elif mod == 'quiz':
                            timeEnd = await self._getTimeEndByQuiz(userName, idLesson)
                            await Hbc_StudentDataApi().register(ropStudent.id, timeEnd)

    async def _getTimeEndByQuiz(self, nameStudent, idQuiz)->str:
        name = nameStudent.split(' ')
        self.info = {'firstInitial': name[1][0], 'lastInitial': name[0][0], 'idQuiz': idQuiz}
        async with self.get('getQuiz') as response:
            text = await response.text()
            trs = await self.findAll(text, 'tr', class_='gradedattempt', 
                                attrs={'id': lambda x: x and x.startswith('mod-quiz')})
            for tr in trs:
                nameStudentDiv = tr.find('td', class_='cell c2 bold').find('a').get_text()
                if (nameStudentDiv == nameStudent):
                    return tr.find('td', class_='cell c5').get_text().strip()

    async def uploadFilesAssigns(self, idStudent):
        lRopStudentLesson = await Hbc_StudentLessonApi().getAllByStudent(idStudent)
        for rop in lRopStudentLesson:
                if not rop.bUploadFile:
                    await self.uploadFilesAssign(rop)

    async def uploadFilesAssign(self, rop: Hbc_StudentLessonApi._classObj):
        ropLesson = await Hbc_LessonApi().load(rop.idLesson)
        self.info = {'idAssign': ropLesson.sIdExit, 
                     'idStudent': (await Hbc_StudentApi().load(rop.idStudent)).sIdNew}
        async with self.get('getAssign') as response:
            text = await response.text()
            for div in await self.findAll(text, 'div', class_='fileuploadsubmission'):
                a = div.find('a')
                async with self.get(a['href']) as responseFile:
                    content = await responseFile.read()
                    await Bc_FileApi().insertBygidSrc(rop.gid, a.get_text(), content)
            
            await self.createCodeWorkspace(rop)
            rop.bUploadFile = 1
            await Hbc_StudentLessonApi().update(rop)
        
    async def createCodeWorkspace(self, rop:Hbc_StudentLessonApi._classObj):
        sHeadLIneLesson = Hbc_LessonApi().calcHeadLine(await Hbc_LessonApi().load(rop.idLesson))
        workspace_data = {
            "folders": [
                {
                    "path": f"../{rop.id}",
                    "name": sHeadLIneLesson
                }
            ],
            "settings": {
                "files.exclude": {
                "**/*.code-workspace": True
                },
                "chat.disableAIFeatures": True,
                "files.autoSave": "onFocusChange",
                "workbench.colorTheme": "Default Dark Modern",
                "editor.fontFamily": "Fira Code, Consolas, monospace",
                "editor.fontSize": 14,
                "security.workspace.trust.enabled": False,
                "extensions.ignoreRecommendations": True,
                "workbench.activityBar.location": "hidden"
            }
        }
        await Bc_FileApi().insertBygidSrc(rop.gid, f'{sHeadLIneLesson}.code-workspace', workspace_data)

    async def fillScore(self, rop):
        info = {'idAssign': (await Hbc_LessonApi().load(rop.idLesson)).sIdExit, 
                'idStudent': (await Hbc_StudentApi().load(rop.idStudent)).sIdNew}
        self.info = info
        async with self.get("getAssign") as response:
            content = await response.text()
            moodle_grade_form_data = {
                "editpdf_source_userid": info['idStudent'],
                "id": info['idAssign'],
                "rownum": "0",
                "useridlistid": "",
                "attemptnumber": "-1",
                "ajax": "0",
                "userid": info['idStudent'],
                "action": "submitgrade",
                "sesskey": (await self.find(content, 'input', attrs={'name': 'sesskey'})).get('value'),
                f"_qf__mod_assign_grade_form_{info['idStudent']}": "1",
                "grade": "2",
                "assignfeedbackcomments_editor[text]": "",
                "assignfeedbackcomments_editor[format]": "1",
                "assignfeedbackcomments_editor[itemid]": "785427455",
                "assignfeedback_editpdf_haschanges": "false",
                "addattempt": "0",
                "sendstudentnotifications": "0",
                "savegrade": "Сохранить"
            }
        self.info = {'attr': ''}
        async with self.post("view", data=moodle_grade_form_data) as response:
            w = await response.text()
            if response.status == 200:
                self.info = {'attr': f'?id={info['idAssign']}&action=savegradingresult'}
                await self.get("view")
                rop.bFillScore = 1
                await Hbc_StudentLessonApi().update(rop)



