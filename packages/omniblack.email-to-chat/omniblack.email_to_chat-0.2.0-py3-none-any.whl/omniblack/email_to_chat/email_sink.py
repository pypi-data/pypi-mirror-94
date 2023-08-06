import ssl
from email import message_from_string, message_from_bytes
from email.message import EmailMessage
from email.policy import SMTPUTF8, strict
from asyncio import create_task, get_running_loop
from logging import getLogger

from aiosmtpd.smtp import SMTP
from aiosmtpd.handlers import AsyncMessage

from .InputSink import InputSink
from .get_fds import get_sockets_from_fds

log = getLogger(__name__)

COMMASPACE = ', '


class ChatHandler(AsyncMessage):
    def __init__(
            self,
            *args,
            queue,
            message_class=None,
            policy=None,
            **kwargs,
    ):
        if message_class is None:
            message_class = EmailMessage

        if policy is None:
            policy = SMTPUTF8 + strict

        super().__init__(*args, message_class=message_class, **kwargs)
        self.policy = policy
        self.queue = queue

    async def handle_message(self, message):
        create_task(self.queue.put(message))

    def prepare_message(self, session, envelope):
        # If the server was created with decode_data True, then data will be a
        # str, otherwise it will be bytes.
        data = envelope.content
        if isinstance(data, bytes):
            message = message_from_bytes(
                data,
                self.message_class,
                policy=self.policy,
            )
        else:
            assert isinstance(data, str), (
                f'Expected str or bytes, got {type(data)}'
            )
            message = message_from_string(
                data,
                self.message_class,
                policy=self.policy,
            )
            message['X-Peer'] = str(session.peer)
            message['X-MailFrom'] = envelope.mail_from
            message['X-RcptTo'] = COMMASPACE.join(envelope.rcpt_tos)
        return message


class Email(InputSink):
    def __init__(
        self,
        *,
        enable_SMTPUTF8=None,
        ssl_context: ssl.SSLContext = None,
        server_kwargs=None,
    ):
        super().__init__()
        self.smtpd = None
        self.server = None
        self.ssl_context = ssl_context
        self.loop = get_running_loop()
        self.server_kwargs = server_kwargs or {}
        self.handler = ChatHandler(queue=self.queue)

        sockets = get_sockets_from_fds()
        self.socket = sockets['email.socket']

    def factory(self):
        """Allow subclasses to customize the handler/server creation."""
        return SMTP(
            self.handler, **self.server_kwargs
        )

    def _factory_invoker(self):
        """Wraps factory() to catch exceptions during instantiation"""
        self.smtpd = self.factory()
        if self.smtpd is None:
            raise RuntimeError("factory() returned None")
        return self.smtpd

    async def start(self):
        log.info('Starting Email Server')
        self.server = await self.loop.create_server(
            self._factory_invoker,
            sock=self.socket,
            ssl=self.ssl_context,
        )

        log.info('Server started')

    async def stop(self):
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()
