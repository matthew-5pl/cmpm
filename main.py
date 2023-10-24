# aisi spaisi! canta una musica pra mim.

import discord
from discord.ext import commands
from pytube import YouTube
import os, sys
import asyncio

queue = []

token = os.getenv('CMPM_TOK')
audio_dir = os.getenv('CMPM_DLP')

intents = discord.Intents.default()
intents.message_content = True

AUDIO_NAME = "audio.mp3"

bot = commands.Bot(command_prefix='%', intents=intents)

done = False

mCtx = None

vc = None

def audio_done(stream, file_path):
    global mCtx
    global done
    done = True
    bot.dispatch("music_dl_done", mCtx)

def audio_title(video_url):
    video = YouTube(video_url)
    return video.title

# def not repurposed (stolen) from https://dev.to/shittu_olumide_/how-to-download-youtube-music-and-videos-with-python-37k5
def dl_audio(video_url, ctx):
    global mCtx
    mCtx = ctx
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio = True).first()

    video.register_on_complete_callback(audio_done)

    try:
        audio.download(output_path=audio_dir, filename=AUDIO_NAME)
    except Exception as e:
        return e

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_music_dl_done(ctx):
    global vc
    global queue
    await ctx.send("done downloading!!")
    voice_channel = ctx.author.voice.channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        if vc == None or not vc.is_connected():
            vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=os.path.join(audio_dir, AUDIO_NAME)))
        while vc.is_playing():
            await asyncio.sleep(.1)
        queue.pop(0)
        if len(queue) == 0:
            await vc.disconnect()
        else:
            done = False
            success = dl_audio(queue[-1], ctx)
            if success:
                await ctx.send(f"sorry pooks {title} was only a munch!! (download failed)")
                done = False
    else:
        await ctx.send("can't play music pooks! please join a vc first...")

@bot.command(brief="Mostra la lista delle canzoni")
async def lista(ctx):
    global queue
    q_str = "here's the queue pooks: \n"
    for pos, val in enumerate(queue):
        q_str += f"{pos}: {val}\n"
    await ctx.send(q_str)

@bot.command(brief="Esci dal canale vocale")
async def ferma(ctx):
    global vc
    if vc != None and vc.is_playing():
        await ctx.send("ok pooks!!! leaving channel...")
        await vc.disconnect()
    else:
        await ctx.send("music is not playing....... flop!")

@bot.command(brief="Salta alla prossima canzone in coda")
async def salta(ctx):
    global vc
    if vc != None and vc.is_connected() and len(queue) > 0:
        queue.pop(0)
        vc.stop()
        done = False
        success = dl_audio(queue[-1], ctx)
        if success:
            await ctx.send(f"sorry pooks {title} was only a munch!! (download failed)")
            done = False
    else:
        await ctx.send("can't skip! queue is empty or not in vc")
            
@bot.command(brief="Metti in pausa la canzone")
async def pausa(ctx):
    global vc
    if vc != None and vc.is_playing() and not vc.is_paused():
        await ctx.send("NOW HOLD AWN")
        vc.pause()
    else:
        await ctx.send("its pawsed or nawt playing......")

@bot.command(brief="Se il bot si inqla, esegui questo comando per riavviarlo")
async def unflop(ctx):
    await ctx.send(f'trying to unflop... {"/usr/bin/python3 " + sys.argv[0]}')
    os.execv("/usr/bin/python3", ["python"] + sys.argv)

@bot.command(brief="Fai ripartire una canzone in pausa")
async def vai(ctx):
    global vc
    if vc != None and vc.is_paused():
        await ctx.send("LETS GO KOREA!!")
        vc.resume()
    else:
        await ctx.send("its nawt pawsed or nawt playing......")

@bot.command(brief="Scarica e riproduci una canzone dal link di Youtube")
async def canta(ctx, arg):
    global vc
    global queue
    global done
    url = arg
    title = audio_title(url)
    print(len(queue))
    if len(queue) == 0:
        await ctx.send(f"i just wanted to tell you, zet... i'm downloading {title}")
        done = False
        success = dl_audio(url, ctx)
        if success:
            await ctx.send(f"sorry pooks {title} was only a munch!! (download failed)")
            await ctx.send(f"{success}")
            done = False
    else:
        await ctx.send(f"added {title} to the queue in posaytion {len(queue)} pooks!")
    queue.append(str(url))


bot.run(token)
