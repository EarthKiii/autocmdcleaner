import discord, os
from discord.ext import commands
bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
@bot.event
async def on_message(message):
    if message.channel.id == 735505544957394984 :
        await message.delete()

bot.run(os.environ['CLEANER'])        
