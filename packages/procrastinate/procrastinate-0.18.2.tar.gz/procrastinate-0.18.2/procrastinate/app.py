import functools
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional, Set

from procrastinate import connector as connector_module
from procrastinate import exceptions, jobs, manager
from procrastinate import retry as retry_module
from procrastinate import schema, utils

if TYPE_CHECKING:
    from procrastinate import tasks, worker

logger = logging.getLogger(__name__)


class App:
    """
    The App is the main entry point for procrastinate integration.

    Instantiate a single `App` in your code
    and use it to decorate your tasks with `App.task`.

    You can run a worker with `App.run_worker`.

    Attributes
    ----------
    tasks : ``Dict[str, tasks.Task]``
        The mapping of all tasks known by the app. Only procrastinate is expected to
        make changes to this mapping.
    builtin_tasks : ``Dict[str, tasks.Task]``
        The mapping of builtin tasks. Use it to programmatically access builtin tasks,
        to defer them.
    job_manager : `manager.JobManager`
        The `JobManager` linked to the application
    """

    @classmethod
    def from_path(cls, dotted_path: str) -> "App":
        """
        Create an :py:class:`App` object by dynamically loading the
        object at the given path.

        Parameters
        ----------
        dotted_path :
            Dotted path to the object to load (e.g.
            ``mymodule.submodule.procrastinate_app``)
        """
        return utils.load_from_path(dotted_path, cls)

    def __init__(
        self,
        *,
        connector: connector_module.BaseConnector,
        import_paths: Optional[Iterable[str]] = None,
        worker_defaults: Optional[Dict] = None,
        periodic_defaults: Optional[Dict] = None,
    ):
        """
        Parameters
        ----------
        connector :
            Typically an `AiopgConnector`. It will be responsible for all communications
            with the database. Mandatory.
        import_paths :
            List of python dotted paths of modules to import, to make sure
            that the workers know about all possible tasks.
            If you fail to add a path here and a worker encounters
            a task defined at that path, the task will be loaded on the
            fly and run, but you will get a warning.
            You don't need to specify paths that you know have already
            been imported, though it doesn't hurt.
            A `App.task` that has a custom "name" parameter, that is not
            imported and whose module path is not in this list will
            fail to run.
        worker_defaults :
            All the values passed here will override the default values sent when
            launching a worker. See `App.run_worker` for details.
        periodic_defaults :
            Parameters for fine tuning the periodic tasks deferrer. Available
            parameters are:

            - ``max_delay``: ``float``, in seconds. When a worker starts and there's
              a periodic task that has not been deferred, the worker will defer the task
              if it's been due for less that this amount of time. This avoids new
              periodic tasks to be immediately deferred just after their first
              deployment. (defaults to 10 minutes)
        """
        from procrastinate import periodic

        self.connector = connector
        self.tasks: Dict[str, "tasks.Task"] = {}
        self.builtin_tasks: Dict[str, "tasks.Task"] = {}
        self.queues: Set[str] = set()
        self.import_paths = import_paths or []
        self.worker_defaults = worker_defaults or {}
        periodic_defaults = periodic_defaults or {}

        self.job_manager = manager.JobManager(connector=self.connector)
        self.periodic_deferrer = periodic.PeriodicDeferrer(
            job_manager=self.job_manager, **periodic_defaults
        )

        self._register_builtin_tasks()

    def task(
        self,
        _func: Optional[Callable] = None,
        *,
        name: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        retry: retry_module.RetryValue = False,
        pass_context: bool = False,
        queue: str = jobs.DEFAULT_QUEUE,
        lock: Optional[str] = None,
        queueing_lock: Optional[str] = None,
    ) -> Any:
        """
        Declare a function as a task. This method is meant to be used as a decorator::

            @app.task(...)
            def my_task(args):
                ...

        or::

            @app.task
            def my_task(args):
                ...

        The second form will use the default value for all parameters.

        Parameters
        ----------
        _func :
            The decorated function
        queue :
            The name of the queue in which jobs from this task will be launched, if
            the queue is not overridden at launch.
            Default is ``"default"``.
            When a worker is launched, it can listen to specific queues, or to all
            queues.
        lock :
            Default value for the ``lock`` (see `Task.defer`).
        queueing_lock:
            Default value for the ``queueing_lock`` (see `Task.defer`).
        name :
            Name of the task, by default the full dotted path to the decorated function.
            if the function is nested or dynamically defined, it is important to give
            it a unique name, and to make sure the module that defines this function
            is listed in the ``import_paths`` of the `procrastinate.App`.
        aliases:
            Additional names for the task.
            The main use case is to gracefully rename tasks by moving the old
            name to aliases (these tasks can have been scheduled in a distant
            future, so the aliases can remain for a long time).
        retry :
            Details how to auto-retry the task if it fails. Can be:

            - A ``boolean``: will either not retry or retry indefinitely
            - An ``int``: the number of retries before it gives up
            - A `procrastinate.RetryStrategy` instance for complex cases

            Default is no retry.
        pass_context :
            Passes the task execution context in the task as first
        """
        # Because of https://github.com/python/mypy/issues/3157, this function
        # is quite impossible to type consistently, so, we're just using "Any"

        def _wrap(func: Callable[..., "tasks.Task"]):
            from procrastinate import tasks

            task = tasks.Task(
                func,
                app=self,
                queue=queue,
                lock=lock,
                queueing_lock=queueing_lock,
                name=name,
                aliases=aliases,
                retry=retry,
                pass_context=pass_context,
            )
            self._register(task)

            return functools.update_wrapper(task, func)

        if _func is None:  # Called as @app.task(...)
            return _wrap

        return _wrap(_func)  # Called as @app.task

    def periodic(self, *, cron: str):
        """
        Task decorator, marks task as being scheduled for periodic deferring (see
        `howto/cron`).

        Parameters
        ----------
        cron :
            Cron-like string. Optionally add a 6th column for seconds.
        """
        return self.periodic_deferrer.periodic_decorator(cron=cron)

    def _register(self, task: "tasks.Task") -> None:
        self.tasks[task.name] = task
        for alias in task.aliases:
            self.tasks[alias] = task
        queue = task.queue
        if queue not in self.queues:
            logger.debug(
                f"Registering queue {queue}",
                extra={"action": "register_queue", "queue": queue},
            )
            self.queues.add(queue)

    def _register_builtin_tasks(self) -> None:
        from procrastinate import builtin_tasks

        builtin_tasks.register_builtin_tasks(self)

    def configure_task(
        self, name: str, *, allow_unknown: bool = True, **kwargs: Any
    ) -> jobs.JobDeferrer:
        """
        Configure a task for deferring, using its name

        Parameters
        ----------
        name : str
            Name of the task. If not explicitly defined, this will be the dotted path
            to the task (``my.module.my_task``)

        **kwargs: Any
            Parameters from `Task.configure`

        Returns
        -------
        ``jobs.JobDeferrer``
            Launch ``.defer(**task_kwargs)`` on this object to defer your job.
        """
        from procrastinate import tasks

        self.perform_import_paths()
        try:
            return self.tasks[name].configure(**kwargs)
        except KeyError as exc:
            if allow_unknown:
                return tasks.configure_task(
                    name=name, job_manager=self.job_manager, **kwargs
                )
            raise exceptions.TaskNotFound from exc

    def _worker(self, **kwargs) -> "worker.Worker":
        from procrastinate import worker

        final_kwargs = {**self.worker_defaults, **kwargs}

        return worker.Worker(app=self, **final_kwargs)

    @functools.lru_cache(maxsize=1)
    def perform_import_paths(self):
        """
        Whenever using app.tasks, make sure the apps have been imported by calling
        this method.
        """
        utils.import_all(import_paths=self.import_paths)
        logger.debug(
            "All tasks imported",
            extra={"action": "imported_tasks", "tasks": list(self.tasks)},
        )

    async def run_worker_async(self, **kwargs) -> None:
        """
        Run a worker. This worker will run in the foreground and execute the jobs in the
        provided queues. If wait is True, the function will not
        return until the worker stops (most probably when it receives a stop signal).
        The default values of all parameters presented here can be overridden at the
        `App` level.

        Parameters
        ----------
        queues : ``Optional[Iterable[str]]``
            List of queues to listen to, or None to listen to every queue (defaults to
            ``None``).
        wait : ``bool``
            If False, the worker will terminate as soon as it has caught up with the
            queues. If True, the worker will work until it is stopped by a signal
            (``ctrl+c``, ``SIGINT``, ``SIGTERM``) (defaults to ``True``).
        concurrency : ``int``
            Indicates how many asynchronous jobs the worker can run in parallel.
            Do not use concurrency if you have synchronous blocking tasks.
            See `howto/concurrency` (defaults to ``1``).
        name : ``Optional[str]``
            Name of the worker. Will be passed in the `JobContext` and used in the
            logs (defaults to ``None`` which will result in the worker named
            ``worker``).
        timeout : ``float``
            Indicates the maximum duration (in seconds) the worker waits between
            each database job poll. Raising this parameter can lower the rate at which
            the worker makes queries to the database for requesting jobs.
            (defaults to 5.0)
        listen_notify : ``bool``
            If ``True``, the worker will dedicate a connection from the pool to
            listening to database events, notifying of newly available jobs.
            If ``False``, the worker will just poll the database periodically
            (see ``timeout``). (defaults to ``True``)
        delete_jobs : ``str``
            If ``always``, the worker will automatically delete all jobs on completion.
            If ``successful`` the worker will only delete successful jobs.
            If ``never``, the worker will keep the jobs in the database.
            (defaults to ``never``)
        """
        self.perform_import_paths()
        worker = self._worker(**kwargs)
        await worker.run()

    async def check_connection_async(self):
        return await self.job_manager.check_connection()

    @property
    def schema_manager(self) -> schema.SchemaManager:
        return schema.SchemaManager(connector=self.connector)

    def open(self, pool: Optional[connector_module.Pool] = None) -> "App":
        self.connector.open(pool)
        return self

    def close(self) -> None:
        self.connector.close()

    def open_async(
        self, pool: Optional[connector_module.Pool] = None
    ) -> utils.AwaitableContext:
        open_coro = functools.partial(self.connector.open_async, pool=pool)
        return utils.AwaitableContext(
            open_coro=open_coro,
            close_coro=self.connector.close_async,
            return_value=self,
        )

    async def close_async(self) -> None:
        await self.connector.close_async()

    def __enter__(self) -> "App":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


utils.add_method_sync_api(cls=App, method_name="run_worker_async")
utils.add_method_sync_api(cls=App, method_name="check_connection_async")
