import discord

helpstring = "Works for both anime and manga.\n 1. Use #anime desc <anime_name> to get the synopsis of an anime.\n 2. Use #anime info <anime_name> to get extended anime information.\n 3. Use #anime recommend <anime_name> to get similar anime recommendations.\n 4. Use #anime trailer <anime_name> to get trailers for the anime.\n 4. Use #anime song <anime_name> to get list of anime openings and endings.\n 5. Use #anime play <song_name> to play the exact song_name as on Youtube.\n 6. Use #anime search <anime_name> to search for an anime (currently being worked on as there are issues).\n We will try our best at maintaining these features and adding more interesting ones, So stay tuned !!!"

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
