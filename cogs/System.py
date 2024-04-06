import discord
from discord.ext import commands
from tts.tts_voices import voice_dict
from models.VoiceList import VoiceList

color = 0x59b19d


class System(commands.Cog):
    voice_clients = {}

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('System.py is ready')

    @commands.command(help='= Shows latency in miliseconds.')
    async def ping(self, ctx):
        emb = discord.Embed(title='Ping', description=f'{round(self.client.latency * 1000)}ms', color=color)
        await ctx.send(embed=emb)

    @commands.command(help='= Shows bitrate of current channel.')
    async def bitrate(self, ctx):
        try:
            if ctx.voice_client.is_connected():
                await ctx.send(f'Current bitrate is: {ctx.author.voice.channel.bitrate / 1000}Kbps')
        except Exception as err:
            print(err)

    @commands.command(aliases=['v'],
                      help='= Shows available voice to use in tts.')
    async def voices(self, ctx):
        try:
            list1 = []
            list2 = []
            for voice in voice_dict:
                list1.append(voice)
                list2.append(voice_dict[voice][5])
            message = VoiceList(list1, list2)
            await message.send(ctx)
        except Exception as err:
            print(err)

    @commands.command(aliases=['h'])
    async def comms(self, ctx):
        try:
            system = '```'
            tts = '```'
            schedule = '```'
            for command in self.client.commands:
                if command.help is not None and command.cog is not None:
                    match command.cog.qualified_name:
                        case 'System':
                            system += f'?{command.name} {command.help}\n\n'
                        case 'Tts':
                            tts += f'?{command.name} {command.help}\n\n'
                        case _:
                            continue
            system += '```'
            tts += '```'
            embed = discord.Embed(title='Commands', color=color)
            embed.add_field(name='TTS', value=tts, inline=False)
            embed.add_field(name='System', value=system, inline=False)
            await ctx.send(embed=embed)
        except Exception as err:
            print(err)


async def setup(client):
    await client.add_cog(System(client))
