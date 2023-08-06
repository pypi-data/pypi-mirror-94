from contextlib import contextmanager
from asyncio import (
    create_task,
    gather,
    run,
    wait,
    FIRST_COMPLETED,
)

from omniblack.logging import config
from logging import getLogger, INFO, captureWarnings

from .discord_sink import Discord
from .email_sink import Email

captureWarnings(True)
log = getLogger()
log.setLevel(INFO)


@contextmanager
def job(queue, result):
    try:
        yield result
    finally:
        queue.task_done()


async def select(*queues):
    tasks = {
        create_task(queue.get()): queue
        for queue in queues
    }

    while queues:
        (done, pending) = await wait(tasks.keys(), return_when=FIRST_COMPLETED)
        for task in done:
            queue = tasks[task]
            del tasks[task]
            new_task = create_task(queue.get())
            tasks[new_task] = queue
            yield job(queue, task.result())


async def process_messages(in_sinks, out_sinks):
    queues = tuple(
        sink.queue
        for sink in in_sinks
    )
    async for job in select(*queues):
        with job as message:
            msg_tasks = (
                sink.on_message(message)
                for sink in out_sinks
            )

            await gather(*msg_tasks)


async def main():
    server_kwargs = dict(enable_SMTPUTF8=True)
    discord = Discord()
    email = Email(server_kwargs=server_kwargs)
    await discord.start()
    await email.start()
    log.info('Sinks started')
    await process_messages((email, ), (discord, ))


def run_email():
    try:
        config()
        run(main())
    except KeyboardInterrupt:
        log.info('Received SIGINT exiting')
        return 0
    except Exception as exception:
        log.critical('Unknown fatal error', exc_info=exception)
        return 1
    return 0


if __name__ == '__main__':
    run_email()
