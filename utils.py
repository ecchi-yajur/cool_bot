import discord

def easyembed(bot , title , description , imgurl = 'none' , thumbnailurl = 'none'):
    embed = discord.Embed()
    embed.title = title
    if(len(description)) > 2048:
        description = description[:2045] + "..."
    embed.description = description
    embed.colour = 0x00FFFF
    embed.set_footer(text = 'cool_bot OwO 🤖')
    if thumbnailurl == 'none':
        embed.set_thumbnail(url = bot.user.avatar_url)
    elif thumbnailurl != 'no':
        embed.set_thumbnail(url = thumbnailurl)
    if imgurl != 'none' :
        embed.set_image(url=imgurl)
    return embed
