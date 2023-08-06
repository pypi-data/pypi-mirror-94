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
from .internal_sink import Internal, InternalMessage
from .heartbeat_sink import HeartBeat

captureWarnings(True)
log = getLogger()
log.setLevel(INFO)


internal_msgs = None


@contextmanager
def job(queue, msg):
    try:
        yield msg
    except Exception as exc:
        if not isinstance(msg, InternalMessage):
            internal_msgs.report_exception(exc, msg)
            extra = dict(failed_msg=msg)
            log.exception('Error occurred while sending message', extra=extra)
        else:
            raise exc
    finally:
        queue.task_done()


async def select(*queues):
    tasks = {
        create_task(queue.get()): queue
        for queue in queues
    }

    while True:
        (done, _pend) = await wait(tasks.keys(), return_when=FIRST_COMPLETED)
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
    global internal_msgs
    internal_msgs = Internal()

    discord = Discord()
    server_kwargs = dict(enable_SMTPUTF8=True)
    email = Email(server_kwargs=server_kwargs)
    heartbeat = HeartBeat()

    await gather(discord.start(), internal_msgs.start(), heartbeat.start())
    await email.start()
    log.info('Sinks started')
    await process_messages((email, internal_msgs, heartbeat), (discord, ))


def run_email():
    try:
        config(system_vital=True, systemd=True)
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
