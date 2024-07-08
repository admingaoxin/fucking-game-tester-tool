import threading
import time
from abc import ABC, abstractmethod


class ITask(ABC):
    @abstractmethod
    def run(self):
        pass


class MyExecServiceV2B:
    def __init__(self, num_threads: int):
        # self.shutdown()
        self.__num_threads = num_threads
        self.__lstth = []
        self.__task_pending = []
        self.__lk_task_pending = threading.Lock()
        self.__cond_task_pending = threading.Condition(self.__lk_task_pending)
        self.__task_running = []
        self.__lk_task_running = threading.Lock()
        self.__cond_task_running = threading.Condition(self.__lk_task_running)
        self.__force_thread_shutdown = False

        for _ in range(self.__num_threads):
            self.__lstth.append(
                threading.Thread(target=MyExecServiceV2B.__thread_worker_func, args=(self,))
            )

        for th in self.__lstth:
            th.start()


    def submit(self, task: ITask):
        with self.__lk_task_pending:
            self.__task_pending.append(task)
            self.__cond_task_pending.notify()


    def wait_task_done(self):
        while True:
            with self.__lk_task_pending:
                if len(self.__task_pending) == 0:
                    with self.__lk_task_running:
                        while len(self.__task_running) > 0:
                            self.__cond_task_running.wait()

                        # no pending task and no running task
                        break


    def shutdown(self):
        if not hasattr(self, f'_{self.__class__.__name__}__lstth'):
            return

        self.__force_thread_shutdown = True

        with self.__lk_task_pending:
            self.__task_pending.clear()
            self.__cond_task_pending.notify_all()

        _ = [th.join() for th in self.__lstth]
        self.__num_threads = 0
        self.__lstth.clear()


    @staticmethod
    def __thread_worker_func(selfptr: 'MyExecServiceV2B'):
        task_pending = selfptr.__task_pending
        lk_task_pending = selfptr.__lk_task_pending
        cond_task_pending = selfptr.__cond_task_pending

        task_running = selfptr.__task_running
        lk_task_running = selfptr.__lk_task_running
        cond_task_running = selfptr.__cond_task_running

        while True:
            with lk_task_pending:
                # WAIT FOR AN AVAILABLE PENDING TASK
                while len(task_pending) == 0 and not selfptr.__force_thread_shutdown:
                    cond_task_pending.wait()

                if selfptr.__force_thread_shutdown:
                    # lk_task_pending.release()
                    break

                # GET THE TASK FROM THE PENDING QUEUE
                task = task_pending.pop(0)

                # PUSH IT TO THE RUNNING QUEUE
                with lk_task_running:
                    task_running.append(task)

            # DO THE TASK
            task.run()

            # REMOVE IT FROM THE RUNNING QUEUE
            with lk_task_running:
                task_running.remove(task)
                cond_task_running.notify()



class RepositoryType:
    HG =0
    GIT = 1
    SVN = 2
    PERFORCE = 3

class Repository():
    _registry = {}

    def __init_subclass__(cls, scm_type=None, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if scm_type is not None:
            if scm_type not in cls._registry:
                cls._registry[scm_type] = {}
            cls._registry[scm_type][name] = cls

class MainHgRepository(Repository, scm_type=RepositoryType.HG, name='main'):
    pass

class GenericGitRepository(Repository, scm_type=RepositoryType.GIT):
    pass
class IgnoreElem():
    """An element of the ignore list"""

    def __init_subclass__(cls, attrs, **kwargs) -> None:
        """Define different attributes for subclasses"""
        super().__init_subclass__(**kwargs)


class IgnoreModule(IgnoreElem, attrs=["module"]):
    """Ignore calls from a module or its submodules"""
    def _post_init(self) -> None:
        pass

    def match(self, frame_no: int, frameinfo) -> bool:
        pass



if __name__ == "__main__":
    class MyTask(ITask):
        def __init__(self, task_id: str):
            self.id = task_id

        def run(self):
            print(f'Task {self.id} is starting')
            time.sleep(3)
            print(f'Task {self.id} is completed')



    NUM_THREADS = 12
    NUM_TASKS = 20
    t = time.time()

    exec_service = MyExecServiceV2B(NUM_THREADS)

    lsttask = [MyTask(chr(i + 65)) for i in range(NUM_TASKS)]

    for task in lsttask:
        exec_service.submit(task)

    print('All tasks are submitted')

    exec_service.wait_task_done()
    print('All tasks are completed')

    exec_service.shutdown()
    print(f"TIME {time.time() -t} s")
