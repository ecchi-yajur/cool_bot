import os
import random

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
			anime = args[2]
			response = anime_desc(anime)
			await ctx.send(response)
		else :
			await ctx.send('invalid')	
	else :
		await ctx.send('invalid')	
bot.run(TOKEN)