import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from scraper import anime_desc,anime_info,anime_search

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='#')

@bot.command(name='anime')
async def cool_bot(ctx,*args):
	if len(args) >1 :
		if args[0] == 'desc':
			anime = " ".join(args[1:])
			response,img = anime_desc(anime)
			embed = discord.Embed()
			embed.title = "anime description"
			embed.description = response
			embed.set_image(url=img)
			embed.colour = 0x00FFFF
			embed.set_footer(text = 'cool_bot OwO 🤖')
			embed.set_thumbnail(url = bot.user.avatar_url)
			await ctx.send(embed = embed)
		elif args[0] == 'info':
			anime = " ".join(args[1:])
			response,img = anime_info(anime)
			embed = discord.Embed()
			embed.title = "anime information"
			embed.description = response
			embed.set_image(url=img)
			embed.colour = 0x00FFFF
			embed.set_footer(text = 'cool_bot OwO 🤖')
			embed.set_thumbnail(url = bot.user.avatar_url)
			await ctx.send(embed = embed)
		elif args[0] == 'search':
			anime = " ".join(args[1:])
			anime_list = anime_search(anime)
			embed = discord.Embed()
			embed.title = "anime search"
			anime_list_str = ""
			i = 1
			for row in anime_list:
				anime_list_str = anime_list_str+str(i)+". "+row+"\n"
				i = i + 1
			embed.description = anime_list_str
			embed.colour = 0x00FFFF
			embed.set_footer(text = 'cool_bot OwO 🤖')
			embed.set_thumbnail(url = bot.user.avatar_url)
			await ctx.send(embed = embed)
		else :
			await ctx.send('invalid')	
	else :
		await ctx.send('invalid')	

@bot.event
async def on_ready():
	print("Bot is ready now !")

bot.run(TOKEN)