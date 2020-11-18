import discord, os
client = discord.Client()
autorizedchannel = [735505544957394984]
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
@client.event
async def on_message(message):
    if message.channel.id in autorizedchannel :
        await message.delete()

client.run('Nzc4Njc1ODMxNzY5MjY4MjM0.X7VcYQ.mj2CTkSJiY6mite7xLSVQkf73v0')        


