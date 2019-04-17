import discord

client = discord.Client()
kanale = []
server = discord.Guild
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))





    server = client.guilds[0]

    for cech in client.guilds:
        print(cech)
        for kanal in cech.channels:
            kanale.append(kanal)



@client.event
async def on_message(message):


    if message.author == client.user:
        return

    print(message.author.name)
    existuje_kanal = False
    for channel in kanale:
        if channel.name == message.author.name.lower():
            await channel.send("HELL YEAH")
            existuje_kanal = True
            break
        print(channel)



    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run("")


'''    if existuje_kanal==False:
        print(server)
        over ={
        discord.Guild.default_role: discord.PermissionOverwrite(read_messages=True),
        discord.Guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        novy = discord.abc.GuildChannel()
        await server.create_text_channel(server, "mvkal", overwrites = over, category="sukromne")
        kanale.append(novy)
#        await kanale[len(kanale)-1].send(None)
#        await kanale[len(kanale)-1].send("i WORK")
        print(kanale[len(kanale)-1])'''