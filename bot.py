import discord, os
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.',intents=intents)
defrole = ""
cmdnames = []
cmdchannels = []

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game('.help'))

@bot.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, name=defrole))

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.channel.id in cmdchannels :
        await message.delete()

@bot.event
async def on_reaction_add(reaction, member):
    if member.bot:
        return
    for nbrole in range(0,len(rolename)):
        classname = 'rolename'+str(nbrole)
        klass = type(classname, (object,), {'id': rolename[nbrole]})
        inst = klass()
        if reaction.emoji == emojis[nbrole]:
            await member.add_roles(inst)

@bot.event
async def on_reaction_remove(reaction, member):
    if member.bot:
        return
    for nbrole in range(0,len(rolename)):
        classname = 'rolename'+str(nbrole)
        klass = type(classname, (object,), {'id': rolename[nbrole]})
        inst = klass()
        if reaction.emoji == emojis[nbrole]:
            await member.remove_roles(inst)
    
@bot.command(brief="Add a cmd/bot channels to the list.", help='Here "<arg>" is the name of the channel you want to add to the list \n For exemple, to add channel nammed "chat" to the list, the command would be ".setcmd chat"')
async def setcmd(ctx, arg):
    global cmdchannels, cmdnames
    if type(arg) is int:
        if arg in cmdnames :
            await ctx.send(arg+' is already a cmd/bot channel !')
        else :
            try :
                cmdchannels.append(arg)
                cmdnames.append(arg)
                await ctx.send(arg+' is now defined as a cmd/bot channel !')
            except AttributeError:
                await ctx.send(arg+' is not a valid channel')        
    else :
        if arg in cmdnames :
            await ctx.send(arg+' is already a cmd/bot channel !')
        else :
            try :
                cmdchannels.append(discord.utils.get(ctx.guild.channels, name=arg).id)
                cmdnames.append(arg)
                await ctx.send(arg+' is now defined as a cmd/bot channel !')
            except AttributeError:
                await ctx.send(arg+' is not a valid channel')
            
@bot.command(brief="Remove a cmd/bot channels from the list.", help='Here "<arg>" is the name of the channel you want to remove from the list \n For exemple, remove a channel nammed "chat" from the list, the command would be ".delcmd chat"')
async def delcmd(ctx, arg):
    global cmdchannels, cmdnames
    if type(arg) is int:
        if arg in cmdnames :
            cmdchannels.remove(arg)
            cmdnames.remove(arg)
            await ctx.send(arg+' is not a cmd/bot channel anymore (removed from list)!')        
        else :
            await ctx.send(arg+' is not a cmd/bot channel or is not a valid channel!')
    else :
        if arg in cmdnames :
            cmdchannels.remove(discord.utils.get(ctx.guild.channels, name=arg).id)
            cmdnames.remove(arg)
            await ctx.send(arg+' is not a cmd/bot channel anymore (removed from list)!')        
        else :
            await ctx.send(arg+' is not a cmd/bot channel or is not a valid channel!')

@bot.command(brief="Show all cmd/bot channels.", help="This command don't need args, it will show all cmd/bot channels in an embed if invoked")
async def listcmd(ctx):
    global cmdnames
    if not cmdnames :
        channelnames = "There is no channel defined as a cmd/bot channel !"
    else :
        channelnames = ""
    for i in range(0,len(cmdnames)):        
        channelnames += cmdnames[i]+'\n'
    embed=discord.Embed()
    embed.add_field(name="CMD/BOT channel list :", value=channelnames, inline=False)
    await ctx.send(embed=embed)

@bot.command(brief="Set the default on join role", help='Here "<arg>" is the role (mention it) you want as on join role \n For exemple, if my on join role is "@member", the command would be ".defaultrole @member"')
async def defaultrole(ctx):
    global defrole
    try :
        defrole = str(ctx.message.role_mentions[0])
        await ctx.send(defrole+' is now the default on join role !')
    except IndexError:
        await ctx.send('no role mentionned !')

@bot.command(brief="Create autorole embed.", help='Here is more complicated command the first arg must be a mentionned role and the second one must be the emoji associated to it, you can repeat this patern as many time as you want \n For exemple, if i have a role "@gamer" and "@nolife", the command would be ".rolepoll @gamer <emoji> @nolife <emoji>"(do not forget space)')
async def rolepoll(ctx, *args):
    global emojis,rolename,test
    emojis = []
    for arg in range(1,len(args),2) :
        emojis.append(args[arg])
    multi = 2
    rolepannel = ""
    rolename = []
    for role in range(0,len(args),2) :
        rolepannel += args[role]+' '+args[role+1]+'\n'
        test = args[role]
        for char in '<>@&':
            test = test.replace(char,'')
        rolename.append(test)
    embed=discord.Embed(title="Choissez votre role :", description=rolepannel)
    message = await ctx.send(embed=embed)
    if emojis :
        for emoji in emojis:
            await message.add_reaction(emoji)

@bot.command(brief="Create a simple poll", help='Here the first args is the question and all the other args are emoji that people can react to show their opinion be carful if your question contain spaces use quotation marks \n For exemple, ".poll "Am I beautiful ?" <emoji> <emoji> ..." note : if their is no emoji it will automatically set a cross mark and a check mark')
async def poll(ctx, *args):
    emojis = []
    for arg in range(1,len(args)) :
        emojis.append(args[arg])
    embed=discord.Embed(title="Votez :", description=args[0])
    message = await ctx.send(embed=embed)
    if emojis :
        for emoji in emojis:
            await message.add_reaction(emoji)
    else:
        await message.add_reaction('✅')
        await message.add_reaction('❎')


bot.run(os.environ['MULTITASK'])
