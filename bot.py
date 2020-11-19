import discord, os
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
@client.event
async def on_message(message):
    if message.channel.id == 735505544957394984 :
        await message.delete()

client.run(os.environ['CLEANER'])        
