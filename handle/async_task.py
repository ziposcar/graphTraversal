import threading

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
        for t in self.tasks:
            t.start()
        if wait:
            for t in self.tasks:
                t.join()
            return self.results
        else:
            return

    def task_fun(self, t_index, *args, **kwargs):
        self.results[t_index] = self.funcs[t_index](*args, **kwargs)
