import config
import threading

multi_process_count = config.getPopParameter()[4]
class AsyncTask:
    def __init__(self):
        self.results = []
        self.funcs = []
        self.tasks = []

    def add(self, func, *args, **kwargs):
        args = [arg for arg in args]
        args.insert(0, len(self.results))
        _thread = threading.Thread(target=self.task_fun, args=args, kwargs=kwargs)
        _thread.setDaemon(True)
        self.tasks.append(_thread)
        self.results.append(None)
        self.funcs.append(func)

    def run(self, wait=True):
        running_tasks = []
        for t in self.tasks:
            t.start()
            running_tasks.append(t)
            if wait and len(running_tasks) % multi_process_count == 0:
                for t in running_tasks:
                    t.join()
                running_tasks = []
        if wait:
            for t in running_tasks:
                t.join()
            return self.results

    def task_fun(self, t_index, *args, **kwargs):
        self.results[t_index] = self.funcs[t_index](*args, **kwargs)
