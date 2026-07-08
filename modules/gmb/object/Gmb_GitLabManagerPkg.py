import gitlab

from modules.bc import Bc_ConfigApi

"""
Старый код, надо переписать под новые реали
"""
class Gmb_GitLabManagerPkg:
    def __init__(self):
        self.gitLab = gitlab.Gitlab(
            url=Bc_ConfigApi().getByMnemocode('baseUrlGitLab').sValue,
            private_token=Bc_ConfigApi().getByMnemocode('privateTokenGitLab').sValue,
            timeout=30,  # таймаут в секундах
            retry_transient_errors=True  # автоматический повтор при 429/5xx
        )

        # Проверка соединения (опционально)
        try:
            self.gitLab.auth()
            user = self.gitLab.user
        except gitlab.exceptions.GitlabAuthenticationError as e:
            exit(1)

    def createMR(self, text:str):
        from modules.gmb import Gmb_ModApi
        d = self._get_dict_text(text)
        url = []
        for i in d['mod']:
            project_id = self._get_project_id_by_name(i)[0]
            try:
                project = self.gitLab.projects.get(project_id)
            except gitlab.exceptions.GitlabGetError:
                raise RuntimeError(f"❌ Проект {project_id} не найден или нет доступа")

            objMod = Gmb_ModApi().getByMnemocode(i)
            if not objMod.sIdGitReviewer:
                Gmb_ModApi().setsIdGitReviewer(objMod, self._find_user_id_by_last_name(objMod.sReviewer))

            # 🛠 4. Данные для MR
            mr_payload = {
                "source_branch": f'iss/{d['type']}/{d['issue'] if d["issue"] != 'notask' else d['text'].replace(' ', '-')}',
                "target_branch": 'main',
                "title": text,
                "description": text,
                "assignee_ids": [self.gitLab.user.id],                                                 # Назначаем на себя
                "reviewer_ids": [objMod.sIdGitReviewer],                                               # ID ревьюверов 
                "remove_source_branch": True,                                                          # Удалить ветку после мерджа
                "squash": True                                                                         # Сквошить коммиты при мердже
            }
            Gmb_ModApi().getByMnemocode(i).sReviewer
            # 🚀 5. Создание MR
            try:
                mr = project.mergerequests.create(mr_payload)
                # insertMR(project_id, mr.iid)
                url.append(mr.web_url)
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