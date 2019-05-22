import config
import threading

class AsyncTask:
    def __init__(self):
        self.results = []
        self.funcs = []
        self.argss = []
        self.kwargss = []
        self.tasks = []
        self.multi_process_count = config.getPopParameter()[4]
        self.free_drivers = [i for i in range(self.multi_process_count)]

    def add(self, func, *args, **kwargs):
        _thread = threading.Thread(target=self.task_fun, args=args, kwargs=kwargs)
        _thread.setDaemon(True)
        self.results.append(None)
        self.funcs.append(func)
        self.argss.append(list(args))
        self.kwargss.append(kwargs)

    def run(self):
        for index, f in enumerate(self.funcs):
            while True:
                if self.multi_process_count > 0:
                    if self.free_drivers == []:
                        raise Exception("none of free_drivers")
                    self.argss[index].insert(0, self.free_drivers[-1])
                    self.free_drivers.pop()
                    _thread = threading.Thread(target=self.task_fun, args=self.argss[index], kwargs=self.kwargss[index])
                    _thread.setDaemon(True)
                    _thread.start()
                    self.tasks.append(_thread)
                    self.multi_process_count -= 1
                    break
        for t in self.tasks:
            t.join()
        return self.results

    def task_fun(self, *args, **kwargs):
        self.results[args[3]] = self.funcs[args[3]](*args, **kwargs)
        self.free_drivers.append(args[0])
        self.multi_process_count += 1
