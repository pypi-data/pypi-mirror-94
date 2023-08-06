from socket import gethostname
from asyncio import create_task

from discord import Intents, Embed
from discord.ext import commands

from .OutputSink import OutputSink
from .creds import load_cred


class Discord(OutputSink):
    def __init__(self):
        super().__init__()
        intents = Intents(dm_messages=True)
        self.bot = commands.Bot(
            command_prefix='$',
            intents=intents,
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

    async def on_message(self, message):
        embed = Embed(
            title=message['subject'],
        )

        embed.add_field(name='From', value=message['From'])
        embed.add_field(name='To', value=message['To'])
        embed.add_field(
            name='Body',
            value=message.get_content(),
            inline=False,
        )
        await self.owner.send(embed=embed)

    async def status(self, ctx):
        await ctx.send(f'Up on {self.hostname}')
