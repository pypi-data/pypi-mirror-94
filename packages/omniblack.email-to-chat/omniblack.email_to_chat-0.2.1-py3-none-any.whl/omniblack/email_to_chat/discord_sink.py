from socket import gethostname
from asyncio import create_task
from io import BytesIO

from discord import Intents, Embed, Status, File, Color
from discord.abc import Messageable
from discord.ext import commands

from .abc import OutputSink, Message, MessageType
from .creds import load_cred

DESCRIPTION_LIMIT = 2048


def wrap_msg(msg):
    return f'```\n{msg}\n```'


type_to_color = {
    MessageType.fatal: Color.from_rgb(255, 0, 0),
    MessageType.heartbeat: Color.green(),
    MessageType.report: Color.dark_magenta(),
    MessageType.error: Color.orange(),
}


WRAPPER_SIZE = len(wrap_msg(''))


class DiscordMessage(Message):
    async def send(self, target: Messageable):
        if isinstance(self.body, str):
            if len(self.body) > DESCRIPTION_LIMIT - WRAPPER_SIZE:
                msg_fit = self.body[:DESCRIPTION_LIMIT - WRAPPER_SIZE]
                embed = self.get_embed_header()
                embed.description = wrap_msg(msg_fit)
                bytes_msg = self.body.encode('utf-8')
                fp = BytesIO(bytes_msg)
                file = File(fp, 'complete_msg.txt')
                await target.send(embed=embed, file=file)
            else:
                embed = self.get_embed_header()
                embed.description = wrap_msg(self.body)
                await target.send(embed=embed)
        else:
            embed = Embed(title=self.type.value)
            for name, field in self.body:
                embed.add_field(name=name, value=field, inline=False)
            self.get_embed_header(embed=embed)
            await target.send(embed=embed)

    def get_embed_header(self, embed=None):
        if embed is None:
            embed = Embed(title=self.type.value)
        embed.add_field(name='User', value=self.user)
        embed.add_field(name='Program', value=self.program)
        embed.add_field(name='Host', value=self.host)
        embed.color = type_to_color[self.type]
        return embed

    @classmethod
    def from_msg(cls, msg):
        return cls(**vars(msg))


class Discord(OutputSink):
    def __init__(self):
        super().__init__()
        intents = Intents(dm_messages=True)
        self.bot = commands.Bot(
            command_prefix='$',
            intents=intents,
            status=Status.online,
        )
        self.bot.command()(self.status)
        self.hostname = gethostname()

    async def start(self):
        token = await load_cred('discord_token')
        self.task = create_task(
            self.bot.start(token, bot=True),
            name='Discord bot execution',
        )
        await self.bot.wait_until_ready()
        await self.bot.change_presence()
        app_info = await self.bot.application_info()
        self.owner = app_info.owner

    async def stop(self):
        await self.bot.close()

    async def on_message(self, message: Message):
        msg = DiscordMessage.from_msg(message)
        await msg.send(self.owner)

    async def status(self, ctx):
        await ctx.send(f'Up on {self.hostname}')


if __name__ == '__main__':
    import code
    code.interact(local=globals())
