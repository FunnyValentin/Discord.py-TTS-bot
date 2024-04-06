import discord
from tts.tts_voices import voice_dict
from tts.request import tts_request
from discord.ext import commands
import random

yellow = 0xe1f229
red = 0xf20000


class Tts(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = {}
        self.voice_clients = {}
        self.ffmpeg_options = {'options': '-vn'}

    def tts_q(self, ctx):
        try:
            if self.queue[ctx.author.voice.channel]:
                queue = self.queue[ctx.author.voice.channel]
                tts_request(queue[0][0], queue[0][1], queue[0][2], queue[0][3])
                player = discord.FFmpegPCMAudio("./tts/message.mp3", **self.ffmpeg_options, executable='ffmpeg\\ffmpeg.exe')
                self.voice_clients[ctx.author.voice.channel].play(player, after=lambda e: self.tts_q(ctx))
                self.queue[ctx.author.voice.channel].pop(0)
        except Exception as err:
            print(err)

    @commands.command(aliases=['t', 'T'],
                      help='<name> <message> = Plays a TTS message. For a random voice write Random.')
    async def tts(self, ctx, name, *, msg):
        try:
            channel = ctx.author.voice.channel
            if channel not in self.voice_clients:
                voice_client = await channel.connect()
                self.voice_clients[channel] = voice_client
                self.queue[channel] = []
        except Exception as err:
            print(err)
            embed = discord.Embed(title='Connect to a channel first', color=red)
            await ctx.send(embed=embed)

        try:
            name = name[0].upper() + name[1:]
            if name == 'Random' or name == 'Rnd':
                name = random.choice(list(voice_dict.keys()))
            elif name not in voice_dict:
                embed = discord.Embed(title='Voice name not found', color=red)
                await ctx.send(embed=embed)
                return
        except Exception as err:
            print(err)

        try:
            if ctx.voice_client.is_playing():
                self.queue[channel].append((msg, voice_dict[name][0], voice_dict[name][1], voice_dict[name][2]))
                emb = discord.Embed(title='Message queued', color=yellow)
                await ctx.send(embed=emb)
                return
            tts_request(msg, voice_dict[name][0], voice_dict[name][1], voice_dict[name][2])
            player = discord.FFmpegPCMAudio("./tts/message.mp3", **self.ffmpeg_options, executable='ffmpeg\\ffmpeg.exe')
            self.voice_clients[channel].play(player, after=lambda e: self.tts_q(ctx))
        except Exception as err:
            print(err)

    @commands.command(aliases=['tq'],
                      help='= Shows the message queue.')
    async def tts_queue(self, ctx):
        try:
            queue = self.queue[ctx.author.voice.channel]
            if queue:
                r = ''
                for i in range(len(queue)):
                    r += f'{i+1}- "{queue[i][0]}"\n'
                embed = discord.Embed(title='Message queue', description=r, color=yellow)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='The message queue is empty', color=red)
                await ctx.send(embed=embed)
        except Exception as err:
            print(err)

    @commands.command(aliases=['tc'],
                      help='= Deletes the message queue. If a quantity is specified, it deletes that amount from the end.')
    async def tts_clear(self, ctx, n=0):
        try:
            queue = self.queue[ctx.author.voice.channel]
            if n == 0:
                self.queue[ctx.author.voice.channel] = []
                embed = discord.Embed(title='Message queue cleared', color=red)
                await ctx.send(embed=embed)
            else:
                self.queue[ctx.author.voice.channel] = queue[:len(queue) - n]
                embed = discord.Embed(title=f'Cleared last {n} messages from queue', color=red)
                await ctx.send(embed=embed)
        except Exception as err:
            print(err)

    @commands.command(aliases=['p', 'P'],
                      help='= Pauses the message. Send pause again to resume.')
    async def pause(self, ctx):
        try:
            voice = self.voice_clients[ctx.author.voice.channel]
            if voice.is_playing():
                voice.pause()
            elif voice.is_paused():
                voice.resume()
        except Exception as err:
            print(err)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tts.py is ready')


async def setup(client):
    await client.add_cog(Tts(client))
