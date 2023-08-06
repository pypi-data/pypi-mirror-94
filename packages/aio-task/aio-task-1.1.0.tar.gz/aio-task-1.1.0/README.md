aio-task
[![pipeline status](https://gitlab.com/cdlr75/aio-task/badges/master/pipeline.svg)](https://gitlab.com/cdlr75/aio-task/commits/master)
[![coverage report](https://gitlab.com/cdlr75/aio-task/badges/master/coverage.svg)](https://gitlab.com/cdlr75/aio-task/commits/master)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Downloads](https://pepy.tech/badge/aio-task)](https://pepy.tech/project/aio-task)
===

Simple and reliable asynchronous tasks manager that is asyncio friendly.


## Key Features

- A simple worker interface to register coroutines as tasks.
- A simple broker interface to produce and fetch tasks.
- Broker and worker(s) can be setup in a single program avoiding external service dependencies (by using dummies queue and cache).
- Task is not lost if worker crash during processing it, it's kept in the queue and re-processed until a worker acknowledge it.
- Task exceptions are not lost: you will retrieve them in the task's result.
- Support rabbitmq, redis and sentinel.
- Easily hackable to add new queuing/caching services


## Getting Started

*Use `docker-compose -f examples/docker-compose.yml up` to bring up a rabbitmq and a redis to run this example.*

#### Install
```
pip install aio-task
```

#### Worker → run tasks
```python
import asyncio
from aio_task import Worker

async def addition(a, b):
    """ Task example. """
    return a + b

async def start_worker():
    rabbitmq_config = {"url": "amqp://guest:guest@localhost:5672",
                       "routing_key": "tasks_queue"}
    redis_config = {"address": "redis://localhost"}
    worker = await Worker.create("rabbitmq", rabbitmq_config,
                                 "redis", redis_config)
    worker.register_handler(addition)
    await worker.start()
    return worker

loop = asyncio.get_event_loop()
worker = loop.run_until_complete(start_worker())

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(worker.close())  # gracefull shutdown

loop.close()
```

#### Broker → produce tasks
```python
import asyncio
from aio_task import Broker

async def sample_addition():
    # setup broker
    rabbitmq_config = {"url": "amqp://guest:guest@localhost:5672",
                       "routing_key": "tasks_queue"}
    redis_config = {"address": "redis://localhost"}
    broker = await Broker.create("rabbitmq", rabbitmq_config,
                               "redis", redis_config)
    # produce task
    task_id = await broker.create_task("addition", {"a": 1, "b": 2})
    await asyncio.sleep(0.1)
    # fetch task
    task = await broker.get_task(task_id)
    print(task)
    await broker.close()  # graceful shutdown

loop = asyncio.get_event_loop()
loop.run_until_complete(sample_addition())
loop.run_until_complete(broker.close())
```

**💡 More examples in examples/ !**


## Run tests

**unit tests**
```
pip install -e .[test]
pytest -xvs tests/unit
```

**integration tests**
```
pip install -e .[test]
docker-compose -f tests/integration/compose/docker-compose.yml up -d
IP_HOST=localhost pytest -xvs tests/integration
```
