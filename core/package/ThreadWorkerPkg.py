import queue
import threading
import traceback


class ThreadWorker:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.thread.start()

    def _worker_loop(self):
        print("Системный поток запущен")
        while True:
            task = self.task_queue.get()
            try:
                if task is None:  # сигнал завершения
                    break

                fun, row, par = task
                fun(*row, **par)

            except Exception as e:
                # Ловим ошибку, чтобы поток не умер.
                # Выводим её в консоль, иначе вы не узнаете, что задача провалилась.
                print(f"[ThreadWorker] Ошибка в задаче: {e}")
                traceback.print_exc()
            finally:
                # Гарантируем, что task_done() вызовется ВСЕГДА,
                # даже если была ошибка или пришел сигнал остановки (None)
                self.task_queue.task_done()

    def submit(self, fun, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        self.task_queue.put((fun, args, kwargs))

    def stop(self):
        self.task_queue.put(None)
        self.thread.join()

    def is_alive(self):
        """Вспомогательный метод для дебага"""
        return self.thread.is_alive()


ThreadWorkerPkg = ThreadWorker()
