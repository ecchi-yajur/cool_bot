import os
import random
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio , FFmpegOpusAudio
from youtube_dl import YoutubeDL
from dotenv import load_dotenv
from scraper import *
from utils import easyembed
import asyncio
from youtube_search import YoutubeSearch
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='#')



@bot.event
async def on_ready():
	print("Bot is ready now !")
	bot.load_extension('cogs.MusicPlayer')


@bot.command(name='anime' , description = 'Runs all anime related commands')
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
		else:
			await ctx.send('invalid ❌')	
	elif len(args) == 1:
		if args[0] == 'owner':
			await ctx.send('I was Coded by EcchiYajur and Shreikthegod 😳')
		else :
			await ctx.send('invalid ❌')
	else:
		await ctx.send('invalid Command ❌')	


bot.run(TOKEN)
