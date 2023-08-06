""" Register handlers to process tasks produced by the broker. """
import logging
from aio_task.utils import load_cache, load_consumer
from aio_task.errors import TaskNotRegistered, TaskAlreadyRegistered


class Worker:
    """ Worker register handlers and consume tasks. """

    def __init__(self):
        self.task = None
        self.queue = None
        self.cache = None
        self._start = False
        self._handlers = {}

    @classmethod
    async def create(cls,
                     queue_type="dummy",
                     queue_conf=None,
                     cache_type="dummy",
                     cache_conf=None):
        """ Create a new consumer instance. """
        worker = cls()
        cache_klass = load_cache(cache_type)
        worker.cache = await cache_klass.create(cache_conf)

        queue_klass = load_consumer(queue_type)
        worker.queue = await queue_klass.create(queue_conf,
                                                callback=worker.on_message)
        logging.info(f"worker ready. cache: {cache_type}, queue: {queue_type}")
        return worker

    async def close(self):
        """ Shutdown. """
        if self.queue is not None:
            await self.queue.close()
        if self.cache is not None:
            await self.cache.close()
        logging.info("worker closed")

    async def start(self):
        """ Start to consumer tasks from the queue. """
        logging.info("starting worker with tasks: %s",
                     list(self._handlers.keys()))
        self._start = True
        await self.queue.start()

    def register_handler(self, coro, task_name=None):
        """ Register a handler that process a task.

        :param coro: coroutine
        :param str task_name: The name under which register the task. Default
            the use the coro.__name__
        :raises: aio_task.errors.TaskAlreadyRegistered: handler already registered for the task
        """
        if self._start:
            raise RuntimeError("Worker is already started")

        name = task_name or coro.__name__
        if name in self._handlers:
            raise TaskAlreadyRegistered(f"Handler for {name} already registered.")
        self._handlers[name] = coro

    async def on_message(self, message):
        """ Receive a new message from the broker. """
        name = message.task_name
        logging.debug(f"processing {name}...")
        try:
            handler = self._handlers[name]
        except KeyError:
            exception = TaskNotRegistered(f"can not processed {name}, no handler...")
            logging.error(exception)
            message.set_task_result(exception)
        else:
            try:
                result = await handler(**message.params)
                message.set_task_result(result)
            except Exception as exc:
                logging.exception(f"Error processing {message.task_name}")
                message.set_task_result(exc)
        finally:
            await self.cache.save_task(message.task)
            await self.queue.ack(message)
            logging.info(f"task {message.task.task_id} processed")
