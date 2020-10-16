import discord

def easyembed(bot , title , description , imgurl = 'none'):
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.colour = 0x00FFFF
    embed.set_footer(text = 'cool_bot OwO 🤖')
    embed.set_thumbnail(url = bot.user.avatar_url)
    if imgurl != 'none' :
        embed.set_image(url=imgurl)
    return embed