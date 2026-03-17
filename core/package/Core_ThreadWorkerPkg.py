import threading
import queue

class ThreadWorker:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.thread.start()
    
    def _worker_loop(self):
        while True:
            task = self.task_queue.get()
            if task is None:  # сигнал завершения
                break
            fun, row, par = task
            fun(*row, **par)
            self.task_queue.task_done()
    
    def submit(self, fun, args=(), kwargs={}):
        self.task_queue.put((fun, args, kwargs))
    
    def stop(self):
        self.task_queue.put(None)
        self.thread.join()

tw = ThreadWorker()