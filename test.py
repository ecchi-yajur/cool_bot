import os
import random
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio , FFmpegOpusAudio
from youtube_dl import YoutubeDL
from dotenv import load_dotenv
from scraper import *
from utils import easyembed,helpstring
import asyncio
from youtube_search import YoutubeSearch
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='#')
players = {}

queue = {} # dict indexed by server id , value is a list of voice clients , key : SERVER_ID , value : [song1 ,song2 , song3....] 
song_tracks = {} # key : server_ID , value : [songtitle1 , songtitle2]

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True' , 'forceip':'4'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn' , }





def check_queue(id):
	if len(queue[id]) > 1 :
		queue[id].pop(0) # remove the current song
		song_tracks[id].pop(0)
		voiceClient = players[id]
		print(f"length of queue is  , key = {id} : {len(queue[id])} \n")
		audioSource = queue[id][0] # pick front most audio source
		voiceClient.play(audioSource, after = lambda x=None : check_queue(id))
	elif len(queue[id]) == 1:
		queue[id].pop(0)
		song_tracks[id].pop(0)
		voiceClient = players[id]
		voiceClient.stop()
		

 

@bot.event
async def on_ready():
	print("Bot is ready now !")


@bot.command(name='anime' ,brief='==> anime/manga + a little bit of music bot', description = 'Runs all anime related commands',help=helpstring)
async def cool_bot(ctx,*args):
	if len(args) >1 :
		if args[0] == 'desc':
			anime = " ".join(args[1:])
			response,img = anime_desc(anime)
			embed = easyembed(bot,"anime description",response,img)
			await ctx.send(embed = embed)
		elif args[0] == 'info':
			anime = " ".join(args[1:])
			response,img = anime_info(anime)
			embed = easyembed(bot , "anime information" , response,img )
			await ctx.send(embed = embed)
		elif args[0] == 'search':
			anime = " ".join(args[1:])
			anime_list = anime_search(anime)
			anime_list_str = ""
			i = 1
			for row in anime_list:
				anime_list_str = anime_list_str+str(i)+". "+row+"\n"
				i = i + 1
			embed = easyembed(bot , "anime search" , anime_list_str )
			await ctx.send(embed = embed)
		elif args[0] == 'recommend':
			anime = " ".join(args[1:])
			anime_list = anime_recommend(anime)
			anime_list_str = ""
			i = 1
			for row in anime_list:
				anime_list_str = anime_list_str+str(i)+". "+row+"\n"
				i = i + 1
			embed = easyembed(bot,"anime recommendations",anime_list_str)
			await ctx.send(embed = embed)
		elif args[0] == 'trailer':
			anime = " ".join(args[1:])
			links = anime_trailer(anime)
			description = ""
			i = 1
			for link in links:
				description += str(i) + ". " +  link + "\n"
				i += 1
			embed = easyembed(bot,"anime trailers" , description)
			await ctx.send(embed=embed)
		elif args[0] == 'song':
			anime = " ".join(args[1:])
			anime_song_str = anime_song(anime)
			embed = easyembed(bot,"anime openings and endings",anime_song_str)
			await ctx.send(embed = embed)
		elif args[0] == 'play':
			search_query = " ".join(args[1:])
			server = ctx.guild
			user = ctx.message.author
			voiceState = user.voice
			if not voiceState :
				await ctx.send('You must be in a voice channel to invoke this command 🔇')
				return
			
			#check if bot is in a voice channel and playing currently

			results = YoutubeSearch(search_query, max_results=10).to_json()
			results = json.loads(results)
			url_suffix = results['videos'][0]['url_suffix']
			video_title = results['videos'][0]['title']
			thumbnail = results['videos'][0]['thumbnails'][0]
			url = 'https://www.youtube.com' + url_suffix 
			title = results['videos'][0]['title']
			with YoutubeDL(YDL_OPTIONS) as ydl:
				info = ydl.extract_info(url, download=False)
			URL = info['formats'][-1]['url']

			if ctx.guild.id in players and players[ctx.guild.id].is_playing():
				# queue the song
				queuedaudioSource = discord.FFmpegOpusAudio(URL , **FFMPEG_OPTIONS)
				queue[ctx.guild.id].append(queuedaudioSource)
				song_tracks[ctx.guild.id].append(title)
				await ctx.send(embed = easyembed(bot,'Music Time 🔈🔉🔊',"Queuing song " + video_title + "..." , thumbnailurl = 'no' , imgurl = thumbnail))
			
			else : # first time 
				#if the bot is already in a voice channel meaning it is in vc but isnt playing anything
				await ctx.send(embed = easyembed(bot,'Music Time 🔈🔉🔊',"playing song " + video_title + "..." , thumbnailurl = 'no' , imgurl = thumbnail))

				if ctx.guild.id in players and players[ctx.guild.id].is_connected():
					voiceClient = players[ctx.guild.id]
				else:
					voiceChannel = voiceState.channel
					voiceClient = await voiceChannel.connect()
					
				audioSource =  discord.FFmpegOpusAudio(URL , **FFMPEG_OPTIONS)
				
				players[ctx.guild.id] = voiceClient
				# fix this mistake here  if some song is loading and another play request is given , it is replaced by the new one
				queue[ctx.guild.id] = [audioSource]
				song_tracks[ctx.guild.id] = [title]
				
				voiceClient.play(audioSource, after = lambda x=None: check_queue(ctx.guild.id))

		else :
			await ctx.send('invalid ❌')	
	elif len(args) == 1:
		if args[0] == 'owner':
			await ctx.send('I was Coded by Shreikthegod 😳')
		elif args[0] == 'stop':
			if ctx.guild.id in players and players[ctx.guild.id].is_playing():
				await players[ctx.guild.id].disconnect()
				await ctx.send("Bot has exited the voice channel.")
			else:
				await ctx.send("Nothing to stop , bot isn't connected to any voice channel ! 🔇")
		elif args[0] == 'queue':
			if ctx.guild.id in queue:
				desc = ""
				i = 1
				for title in song_tracks[ctx.guild.id]:
					desc += str(i) + ". " + title + "\n"
					i += 1
				embed = easyembed(bot,"Currently Queued songs" , desc)
				await ctx.send(embed = embed)
			else:
				await ctx.send('There is no queue , you dum-dum ')
		else :
			await ctx.send('invalid ❌')
	else:
		await ctx.send('invalid Command ❌')	


bot.run(TOKEN)
