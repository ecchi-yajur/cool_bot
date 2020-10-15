import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from scraper import anime_desc,anime_info

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
			await ctx.send(embed = embed)
		else :
			await ctx.send('invalid')	
	else :
		await ctx.send('invalid')	

@bot.event
async def on_ready():
	print("Bot is ready now !")

bot.run(TOKEN)
