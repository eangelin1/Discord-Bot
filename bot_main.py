import discord
import logging
import wikipedia
import requests
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pafy
import random
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import aiohttp
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='$',intents=discord.Intents.all())

bot.remove_command('help')

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

f = open("./assets/tokens.json")
data = json.load(f)

ytApiKey = data['ytApiKey']
discordApiKey = data['discordApiKey']

logging.basicConfig(level=logging.INFO)

client = discord.Client(intents=discord.Intents.all())

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "assets/client_secret_733672119659-964kqb362o0bfqhpgi48ng121d61qq54.apps.googleusercontent.com.json"

random.seed()

# API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = ytApiKey)

async def YtSearch(query):
    # 'request' variable is the only thing you must change
    # depending on the resource and method you need to use
    # in your query
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query
    )
    response = request.execute()

    return response

async def YtVideo(videoId):
    request = youtube.videos().list(
        part="liveStreamingDetails",
        id=videoId
    )
    response = request.execute()
    return response

async def Play(videoId, ctx):
    vc = ctx.voice_client
    url = "https://www.youtube.com/watch?v="+videoId

    try:
        video = pafy.new(url)
 
        audio = video.getbestaudio()
        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)

        vc.play(source)
    except Exception as e:
        await ctx.send(f"Sorry this video couldn't be played:")


async def WikipediaSearch(query):
    results = wikipedia.search(query, results=10, suggestion=False)
    return results

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@bot.event
async def on_message(message):
    if message.content.find("https://tenor.com/view/") != -1:
        await message.channel.send("Yeah haha good one :neutral_face:")

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, e):
        await ctx.send(f"Command '{ctx.message.content}' not recognized.. UwU...")


@bot.command()
async def help(ctx):
    await ctx.send(
        '$hello         = HIII\n'+
        '$yt -query     = Search YouTube for videos matching the query\n'+
        '$brap          = BRAAAPPP\n'+
        '$snifff        = SNIFF SNFFF **SNIIFF**\n'+
        '$leave         = Makes me leave your voice channel :cry:\n' +
        '$cat           = Random cat pic and (***possibly morbid***) cat fact :3\n' +
        '$storm         = Chill storm sounds to vibe and relax to\n' +
        '$wiki -query   = *Knowledge for you, sir* >w<'
    )

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def yt(ctx,*query):

        vc = ctx.voice_client

        if(vc != None):
            if(vc.is_playing()):
                vc.stop()

        if(ctx.author.voice is None):
            await ctx.send("You are not in a voice channel ~.~")
            return

        authorChannel = ctx.author.voice.channel
        
        if(not ctx.voice_client):
            vc = await authorChannel.connect()
        else:
            vc = ctx.voice_client

        
        searchResult = await YtSearch(query)
        videoId = searchResult["items"][0]["id"]["videoId"]

        url = "https://www.youtube.com/watch?v="+videoId

        await Play(videoId, ctx)

        await ctx.send(url)

@bot.command()
async def brap(ctx):

        vc = ctx.voice_client

        if(vc != None):
            if(vc.is_playing()):
                vc.stop()

        if(ctx.author.voice is None):
            await ctx.send("You are not in a voice channel ~.~")
            return

        authorChannel = ctx.author.voice.channel
        
        if(not ctx.voice_client):
            vc = await authorChannel.connect()
        else:
            vc = ctx.voice_client

        await Play('4gcs5k8n-FY',ctx)

@bot.command()
async def snifff(ctx):

        vc = ctx.voice_client

        if(vc != None):
            if(vc.is_playing()):
                vc.stop()

        if(ctx.author.voice is None):
            await ctx.send("You are not in a voice channel ~.~")
            return
        authorChannel = ctx.author.voice.channel
        
        if(not ctx.voice_client):
            vc = await authorChannel.connect()
        else:
            vc = ctx.voice_client

        await Play('gvSnBjaiXXs',ctx)

@bot.command()
async def leave(ctx):
        vc = ctx.voice_client
        if(vc != None):
            await vc.disconnect()
        else:
            await ctx.send("Wow you really tried to make me leave a voice chat I'm not even in... ok... I get it...")

@bot.command()
async def stop(ctx):
        vc = ctx.voice_client
        if(vc != None):
            vc.stop()
        else:
            await ctx.send("I'm not playing music dummyhead ^_^")

@bot.command()
async def number(ctx):
        # random number from 10 - 999
        num = str(random.randint(10, 999))
        await ctx.send("Hehe here's your number\n"+num)

@bot.command()
async def cat(ctx):
        
       async with aiohttp.ClientSession() as session:
          request = await session.get('https://some-random-api.ml/img/cat')
          dogjson = await request.json()
          # This time we'll get the fact request as well!
          request2 = await session.get('https://some-random-api.ml/facts/cat')
          factjson = await request2.json()
          msg1 = dogjson['link']
          msg2 = factjson['fact']
          await ctx.send(msg1)
          await ctx.send(msg2)

@bot.command()
async def storm(ctx):

        vc = ctx.voice_client

        if(vc != None):
            if(vc.is_playing()):
                vc.stop()

        if(ctx.message.author.voice is None):
            await ctx.send("You are not in a voice channel ~.~")
            return
        authorChannel = ctx.author.voice.channel
        
        if(not ctx.voice_client):
            vc = await authorChannel.connect()
        else:
            vc = ctx.voice_client

        await Play("nDq6TstdEi8", ctx)

@bot.command()
async def wiki(ctx,*query):
        query = " ".join(query)
        results = await WikipediaSearch(query)

        await ctx.send("https://en.wikipedia.org/wiki/"+results[0])



bot.run(discordApiKey)