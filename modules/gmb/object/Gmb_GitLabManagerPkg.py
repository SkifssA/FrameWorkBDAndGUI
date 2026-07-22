import gitlab

from modules.bc import Bc_ConfigApi
from engine.package.AsynRunPkg import asyncRun
import time

class Gmb_GitLabManagerPkg:
    def __init__(self):
        self.gitLab = gitlab.Gitlab(
            url=Bc_ConfigApi().getByMnemocode('gmb baseUrlGitLab').sValue,
            private_token=Bc_ConfigApi().getByMnemocode('gmb privateTokenGitLab').sValue,
            timeout=30,  # таймаут в секундах
            retry_transient_errors=True  # автоматический повтор при 429/5xx
        )

        # Проверка соединения (опционально)
        try:
            self.gitLab.auth()
            user = self.gitLab.user
        except gitlab.exceptions.GitlabAuthenticationError as e:
            pass

    def createMR(self, idTask:int, text, branch):
        from modules.gmb import Gmb_ModApi, Gmb_TaskDetApi
        d = asyncRun(Gmb_TaskDetApi()._findAllByAttr('idTask', idTask))
        for i in d:
            objTaskDet = Gmb_TaskDetApi().load(i)
            objMod = Gmb_ModApi().load(objTaskDet.idMod)
            project_id = self._get_project_id_by_name(objMod.sCaption)[0]
            try:
                project = self.gitLab.projects.get(project_id)
            except gitlab.exceptions.GitlabGetError:
                raise RuntimeError(f"❌ Проект {project_id} не найден или нет доступа")

            if not objMod.sIdGitReviewer:
                Gmb_ModApi().setsIdGitReviewer(objMod, self._find_user_id_by_last_name(objMod.sReviewer))

            # 🛠 4. Данные для MR
            mr_payload = {
                "source_branch": branch,
                "target_branch": 'main',
                "title": text,
                "description": text,
                "assignee_ids": [self.gitLab.user.id],                                                 # Назначаем на себя
                "reviewer_ids": [objMod.sIdGitReviewer],                                               # ID ревьюверов 
                "remove_source_branch": True,                                                          # Удалить ветку после мерджа
                "squash": True                                                                         # Сквошить коммиты при мердже
            }
            # 🚀 5. Создание MR
            try:
                mr = project.mergerequests.create(mr_payload)
                # insertMR(project_id, mr.iid)
                objTaskDet.sIdMR = mr.iid
                Gmb_TaskDetApi().update(objTaskDet)
                pass
            except gitlab.exceptions.GitlabCreateError as e:
                pass
            except Exception as e:
                pass

    def _find_user_id_by_last_name(self, last_name: str):
        """
        Ищет пользователя по фамилии и возвращает его ID.

        Предупреждение: Если найдено несколько пользователей, функция вернет ID первого
        и выведет список всех найденных.
        """
        try:
            # Выполняем поиск по фамилии
            users = self.gitLab.users.list(search=last_name)
            
            if not users:
                print(f"❌ Пользователи с фамилией '{last_name}' не найдены.")
                return None

            if len(users) == 1:
                user = users[0]
                print(f"✅ Найден пользователь: {user.name} (username: {user.username})")
                return user.id
            else:
                # Найдено несколько пользователей
                print(f"⚠️ Найдено несколько пользователей по запросу '{last_name}':")
                for u in users:
                    print(f"   - ID: {u.id}, Имя: {u.name}, Username: {u.username}")
                
                # Вы можете реализовать свою логику выбора, например, выбрать первого
                chosen_user = users[0]
                print(f"→ Выбран пользователь: {chosen_user.name} (ID: {chosen_user.id})")
                return chosen_user.id
                
        except gitlab.exceptions.GitlabError as e:
            print(f"Ошибка при поиске: {e}")
            return None

    def _get_project_id_by_name(self, exact_name, namespace=None):
        """
        Ищет проект по точному имени.
        Если указан namespace, ищет только внутри него (например, 'team-a/backend').
        """
        # Получаем проекты (нечёткий поиск)
        candidates = self.gitLab.projects.list(search=exact_name, per_page=100, simple=True)
        
        # Фильтруем точные совпадения по имени
        matches = [p for p in candidates if p.name.lower() == exact_name.lower()]
        
        # Если задан namespace, сужаем поиск
        if namespace:
            matches = [p for p in matches if p.path_with_namespace.lower().startswith(namespace.lower())]
        
        if not matches:
            return None, None
        if len(matches) > 1:
            print(f"⚠️ Найдено {len(matches)} проектов с именем '{exact_name}'.")
            for p in matches:
                print(f"   • {p.path_with_namespace} (ID: {p.id})")
            return matches[0].id, matches[0].path_with_namespace
        
        p = matches[0]
        return p.id, p.path_with_namespace
    
    def MRMonitor(self):
        from modules.gmb import Gmb_ModApi, Gmb_TaskDetApi, Gmb_TaskApi
        print("Проверка выполнения отложеного скрипта из Pkg")
        if int(Bc_ConfigApi().getByMnemocode('gmb beginHourWork').sValue) <= time.localtime().tm_hour <= int(Bc_ConfigApi().getByMnemocode('gmb endHourWork').sValue):
                for i in Gmb_TaskDetApi().getAll():
                    objTaskDet = Gmb_TaskDetApi().load(i['id'])
                    # --- 1. Получаем проект и конкретный MR ---
                    objMod = Gmb_ModApi().load(objTaskDet.idMod)
                    idMod = self._get_project_id_by_name(objMod.sCaption)[0]
                    project = self.gitLab.projects.get(idMod)
                    mr = project.mergerequests.get(objTaskDet.sIdMR)

                    text_fields = None
                    if mr.state == 'merged':
                        text_fields = ['MR приняли', f'Для модуля {project.name} приняли MR']
                        Gmb_TaskApi().delete(Gmb_TaskApi().load(objTaskDet.idTask))

                    if ((x:=self.getLastComm(mr)) is not None):
                        if x['id'] != i['lastComment']:
                            text_fields = ['Новый кометарий MR', f'Для модуля {project.name.lower()} новый коментарий']
                            Gmb_TaskDetApi().setsLastComment(objTaskDet, x['id'])

                    if text_fields is not None:
                        from engine.package.ToasterPkg import ToasterPkg
                        ToasterPkg().text(text_fields).show()
                        

    def getLastComm(self, mr)->dict|None:
        comments = []
        for note in mr.notes.list(all=True):
            if not note.system:
                comments.append({
                    'id': note.id,
                    'author': note.author['username'],
                    'text': note.body,
                    'created_at': note.created_at
                })
        
        # Сортируем по времени
        comments.sort(key=lambda x: x['created_at'])

        return comments[-1] if comments else None