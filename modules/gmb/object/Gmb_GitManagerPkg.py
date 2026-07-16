import git
import subprocess
from multiprocessing import Pool, cpu_count
from pathlib import Path

from modules.bc import Bc_ConfigApi

def GitFabric(lNameModule: list=None):
    modules = [str(item) for item in Path(Bc_ConfigApi().getByMnemocode('gmb modulesRootPath').sValue).iterdir()
               if item.is_dir() and (item / '.git').exists() and (lNameModule is None or str(item)[str(item).rfind('\\')+1:] in lNameModule)]

    if (lNameModule is None):
        with Pool(processes=cpu_count()) as pool:
            modules = pool.map(check_module, modules)
        

    return [Gmb_GitManagerPkg(p) for p in modules if p is not None]

def check_module(module_path):
    print(module_path)
    if Gmb_GitManagerPkg.has_unpushed(module_path):
        return module_path
    return None

class Gmb_GitManagerPkg:
    def __init__(self, repos_dir:str):
        try:
            self.repo = git.Repo(repos_dir)
            self.name = repos_dir[repos_dir.rfind('\\')+1:]
        except git.exc.InvalidGitRepositoryError:
            pass

    def select_branch(self, nameBranches:str):
        self.repo.git.checkout(nameBranches)

    def create_branch(self, nameBranches:str):
        self.repo.git.checkout('-b', nameBranches)

    def get_all_branches(self):
        return list(b.name for b in self.repo.branches)
    
    def delete_branches(self, nameBranches):
        current_branches = self.repo.active_branch.name
        if current_branches == nameBranches:
            self.select_branch('main')
        self.repo.git.branch('-D', nameBranches)

    def has_unpushed_in_main(self):
        self.select_branch('main')
        count = int(self.repo.git.rev_list('--count', 'origin/main..main'))
        return count > 0
    
    def rename_last_commit(self, new_message: str):
        """Переименовывает последний (не запушенный) коммит."""
        self.repo.git.commit('--amend', '-m', new_message)

    def push_new_branch(self, branch_name: str = None):
        """Пушит новую ветку на origin с настройкой отслеживания."""
        # -u связывает локальную ветку с удалённой
        self.repo.git.push('-u', 'origin', branch_name)

    def delete_last_commit_keep_dirty(self) -> bool:
        """
        Удаляет последний коммит, но сохраняет все незакоммиченные изменения.
        Возвращает True если всё прошло чисто, False если был конфликт.
        """
        # 1. Проверка: есть ли коммиты для отката
        try:
            self.repo.git.rev_parse("HEAD~1")
        except git.GitCommandError:
            return False  # Нет предыдущего коммита
            
        # 2. Проверяем, есть ли незакоммиченные изменения
        has_dirty = self.repo.is_dirty(untracked_files=True)
        
        if has_dirty:
            # Сохраняем ВСЁ, что не закоммичено (включая новые файлы)
            self.repo.git.stash('push', '--include-untracked', '-m', '_workflow_uncommitted')
            
        # 3. Удаляем коммит. Теперь рабочая директория "чистая" относительно этого коммита
        self.repo.git.reset('--hard', 'HEAD~1')
        
        # 4. Восстанавливаем незакоммиченные изменения
        if has_dirty:
            try:
                self.repo.git.stash('pop')
                return True  # Всё прошло идеально
            except git.GitCommandError:
                # Конфликт при наложении. Данные в безопасности в stash!
                # Пользователь может достать их вручную: git stash show -p | git apply -3
                return False  
                
        return True

    def allProcces(self, nameBranche:str, nameCommit:str):
        self.create_branch(nameBranche)
        self.rename_last_commit(nameCommit)
        self.push_new_branch(nameBranche)
        self.select_branch('main')
        self.delete_last_commit_keep_dirty()

    @classmethod
    def has_unpushed(cls, repo_path):
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', 'origin/main..main', '--oneline'],
                capture_output=True, text=True, check=False, encoding='utf-8'
            )
            return bool(result.stdout.strip())
        except:
            return False