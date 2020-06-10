from discord.ext import commands
import discord

startup_channel = "General"
sounds_folder = 'extensions/music/sounds/'

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vclient = None
    
    @commands.command(name='voice-connect', aliases=['connect'])
    async def vc_connect(self, ctx, channelName='General'):
        if channelName == None:
            await ctx.send(f'{ctx.author.mention} No voice channel selected.')
            return 

        channel = None

        for vc in ctx.guild.voice_channels:
            if channelName == vc.name:
                channel = vc

        if channel == None:
            await ctx.send(f'{ctx.author.mention} Voice channel "{channelName}" not found.')
            return

        try:
            self.vclient = await channel.connect()
        except Exception as e:
            print(e)
            
        await ctx.send(f'{ctx.author.mention} Bot is connected to voice channel "{channelName}".')

    @commands.command(name='voice-disconnect', aliases=['disconnect'])
    async def vc_disconnect(self, ctx):
        await self.vclient.disconnect()
    
    @commands.command(name='play')
    async def play(self, ctx, songName=None):
        if not self.vclient or not self.vclient.is_connected():
            await ctx.send(f'{ctx.author.mention} Bot is not in any voice channel.')
            return
        
        if songName == None:
            await ctx.send(f'{ctx.author.mention} No soundbite selected.')
            return

        try:
            source = discord.FFmpegPCMAudio(sounds_folder+f'{songName}.mp3')

            if not self.vclient.is_playing():
                self.vclient.play(source, after=None)
        except Exception as e:
            print(e)


    @commands.command(name='stop')
    async def stop(self, ctx):
        if not self.vclient or not self.vclient.is_connected():
            await ctx.send(f'{ctx.author.mention} Bot is not connected to any voice channel.')
            return
        
        if self.vclient.is_playing():
            self.vclient.stop()
            await ctx.send(f'{ctx.author.mention} Stopped.')
        else:
            await ctx.send(f'{ctx.author.mention} No soundbite currently playing.')
        


def setup(bot):
    bot.add_cog(MusicPlayer(bot))

