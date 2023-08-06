from .abc import InputSink, MessageType, LocalMessage, Message
from textwrap import dedent

message_body = dedent("""
    An unhandled execution occurred while trying to send a message.
    A log message has been written to standard out on this host.
""").strip()


class InternalMessage(LocalMessage):
    pass


class Internal(InputSink):
    def report_exception(self, exc: Exception, failed_msg: Message):
        print('Exception reviced')
        msg = LocalMessage(
            type=MessageType.error,
            program='Email To Chat',
            body=(
                ('Message', message_body),
                ('Original User', failed_msg.user),
                ('Original Host', failed_msg.host),
                ('Original Program', failed_msg.program),
                ('Error Message', f'`{repr(exc)}`'),
            ),
        )

        self.queue.put_nowait(msg)

    # There is no setup work needed for the Internal Message queue
    async def start(self):
        pass

    async def stop(self):
        pass
