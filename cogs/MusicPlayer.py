from discord.ext import commands
import lavalink
from discord import utils
from discord import Embed
from utils import easyembed



class MusicCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.music = lavalink.Client(self.bot.user.id)
    self.bot.music.add_node('localhost', 9099, 'youshallnotpass', 'na', 'music-node')
    self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
    self.bot.music.add_event_hook(self.track_hook)

  @commands.command(name='play')
  async def play(self, ctx, *, query):
    try:
      member = ctx.message.author
      if member is not None and member.voice is not None:
        vc = member.voice.channel
        player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        if not player.is_connected:
          player.store('channel', ctx.channel.id)
          await self.connect_to(ctx.guild.id, str(vc.id))
      else:
        await ctx.send('You must be in a voice channel to invoke this command 🔇')
        return

      player = self.bot.music.player_manager.get(ctx.guild.id)
      query = f'ytsearch:{query}'
      results = await player.node.get_tracks(query)
      tracks = results['tracks'][0:10]
      i = 0
      query_result = ''
      for track in tracks:
        i = i + 1
        query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
      embed = easyembed(self.bot , 'Search Results' ,query_result )

      await ctx.channel.send(embed=embed)

      def check(m):
        return m.author.id == ctx.author.id
      
      response = await self.bot.wait_for('message', check=check)
      track = tracks[int(response.content)-1]
      player.add(requester=ctx.author.id, track=track)

      if not player.is_playing:
        await player.play()
        current_track = player.current
        yt_id = current_track.uri.split('=')[1]
        thumbnail_url = 'https://img.youtube.com/vi/' + yt_id +  '/0.jpg'
        await ctx.send(embed = easyembed(self.bot,'Music Time 🔈🔉🔊',"Playing song " + track['info']['title'] + "..." , imgurl = thumbnail_url  , thumbnailurl = 'no'))
      else:
        latest_track = player.queue[-1]
        yt_id = latest_track.uri.split('=')[1]
        thumbnail_url = 'https://img.youtube.com/vi/' + yt_id +  '/0.jpg'
        await ctx.send(embed = easyembed(self.bot,'Music Time 🔈🔉🔊',"Queuing song " + track['info']['title'] + "..." , thumbnailurl= 'no' , imgurl = thumbnail_url ))

    except Exception as error:
      print(error)
  
  @commands.command(name='queue')
  async def queue(self , ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    queue = player.queue
    i = 1
    queue_desc = ""
    for track in queue:
      queue_desc += f"{i}) {track.title}\n"
      i += 1
    embed = easyembed(self.bot , 'Currently Queued Songs',queue_desc)
    await ctx.send(embed = embed)

  async def track_hook(self, event):
    if isinstance(event, lavalink.events.QueueEndEvent):
      guild_id = int(event.player.guild_id)
      await self.connect_to(guild_id, None)
      
  async def connect_to(self, guild_id: int, channel_id: str):
    ws = self.bot._connection._get_websocket(guild_id)
    await ws.voice_state(str(guild_id), channel_id)

  @commands.command(name='stop')
  async def stop(self , ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    await player.stop()
  
  @commands.command(name = 'skip')
  async def skip(self , ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    await ctx.send('Skipping current song...')
    await player.skip()
  
  @commands.command(name = 'pause')
  async def pause(self , ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    await ctx.send('Player paused ⏸🔇')
    await player.set_pause(True)
  
  @commands.command(name = 'resume')
  async def resume(self , ctx):
    player = self.bot.music.player_manager.get(ctx.guild.id)
    await ctx.send('Player resuming 🔈🔉🔊... ')
    await player.set_pause(False)


def setup(bot):
  bot.add_cog(MusicCog(bot))
