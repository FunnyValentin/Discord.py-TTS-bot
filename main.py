import discord
from discord.ext import commands
import os
import asyncio
import datetime

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())


@client.event
async def on_ready():
    now = datetime.datetime.now()
    await client.change_presence(activity=discord.Game(f'Online since {now.strftime("%d-%m-%Y %H:%M:%S")}'))
    print(f'{client.user} is online!')


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')


async def main():
    async with client:
        await load()
        await client.start("TTS_BOT_TOKEN")


if __name__ == '__main__':
    asyncio.run(main())

