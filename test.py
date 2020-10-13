import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from scraper import anime_desc

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='#')

@bot.command(name='cool')
async def cool_bot(ctx,*args):
	if len(args) >=2 :
		if args[0] == 'anime' and args[1] == 'desc':
			anime = " ".join(args[2:])
			response = anime_desc(anime)
			embed = discord.Embed()
			embed.title = "anime description"
			embed.description = response
			embed.colour = 0x17700b
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