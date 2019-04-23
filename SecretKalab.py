import discord
import random
import queue
import asyncio
client = discord.Client()
kanale = []
server = discord.Guild
hraci = []
roles = []
players = []
hlasy = []
creator=discord.member
running = False
commands = asyncio.Queue()

def refresh_kanalov():
    print("refresh")
    global privatny
    for cech in client.guilds:
        print(cech)
        for kanal in cech.channels:
            kanale.append(kanal)
            print("kanal: " + kanal.name)
#            if kanal.name=="sukromne":
 #               privatny = kanal
  #              print(privatny)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))





    
    server = client.guilds[0]
    refresh_kanalov()
    running=False





@client.event
async def on_message(message):
    global running
    global public_channel
    global privatny
    if message.author == client.user:
        return

    print(message.author.name)
    existuje_kanal = False
    for channel in kanale:
        if channel.name == message.author.name.lower():
            existuje_kanal = True
            break
    if not existuje_kanal:
#        await message.channel.send(message.author.name + ", you don't have private channel with me, named " + message.author.name.lower() + 
#        ", so you won't be able to join any game, unless you create one :)")
        overwrites = {
        message.channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        message.channel.guild.me: discord.PermissionOverwrite(read_messages=True),
        message.author: discord.PermissionOverwrite(read_messages=True)
        }

            #await server.create_text_channel('secret', overwrites=overwrites)
        novy = await message.guild.create_text_channel(message.author.name.lower(), overwrites=overwrites)
        #novy = client.start_private_message(message.author)
        await novy.send("jiha :D here ya'll get your personal info you can't share ")
        refresh_kanalov()



    if not message.content.startswith('$'):
        return



    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


    elif message.content == "$join":
        if running:
            if message.channel==public_channel:
                if not message.author.name.lower() in hraci:
                    hraci.append(message.author.name.lower())
                    await message.channel.send(message.author.name + " has just joined succesfully")
                else:
                    await message.channel.send(message.author.name + " is already in the joined players list.")

    elif message.content == "$create":

        if running == False:
            for x in hraci:
                hraci.pop(0)
            creator=message.author
            public_channel=message.channel
            running = True
            await message.channel.send(message.author.name + " just created a game in this channel. Everyone can now join it!")
            hraci.append(message.author.name.lower())
        else:
            await message.channel.send("Game is already running.. wait for its end please")

    
    elif message.content == "$start":
        if len(hraci)>=5 and running:
            await message.channel.send("Let the game... begin!")
            await play(hraci)
        else:
            await message.channel.send("Not enough players are joined :(. Looks like you have less than 5 friends.")


    elif message.content == "$delete":
        if message.author==creator:
            await message.channel.send("Well, game was just deleted..")
            running = False

    elif message.content == "$fill":
        dummici = ['a', 'b', 'c', 'd', 'e']
        for i in dummici:
            print(i)
            hraci.append(i)
            for channel in kanale:
                if channel.name == str(i):
                    existuje_kanal = True
                    break
            if not existuje_kanal:
#               await message.channel.send(message.author.name + ", you don't have private channel with me, named " + message.author.name.lower() + 
#               ", so you won't be able to join any game, unless you create one :)")
                overwrites = {
                message.channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.channel.guild.me: discord.PermissionOverwrite(read_messages=True),
                message.author: discord.PermissionOverwrite(read_messages=True)
                }

                #await server.create_text_channel('secret', overwrites=overwrites)
                novy = await message.guild.create_text_channel(i, overwrites=overwrites)
                #novy = client.start_private_message(message.author)
                await novy.send("jiha :D here ya'll get your personal info you can't share ")
                refresh_kanalov()


    else:
        to_send=message.content[1:]
        await commands.put(to_send, message.author.name)
        print("putujem " + to_send)




    
    

async def send(recepient, content, *texty):
    global public_channel
    for text in texty:
        content = content + text + ' '
    print("chcem sendnut do channelu:'" + recepient + "'")
    if recepient == "Everyone":
        await public_channel.send(content)
    for channel in kanale:
        if channel.name == recepient:
            print("poslal" + content)
            await channel.send(content)

########################################################################################################################################################

async def play(gamers):
    players = gamers
    print("hrac 1 je : " + players[0])
    l = ()
    discard = []
    lib, fas = 0, 0
    global roles
    fascists, liberals = [], []
    fascistNumber = await giveRoles(len(players))
    president, chancellor, lastPresident, lastChancellor = 0, 0, 0, 0
    end = False
    lastVoting = True
    specialGovernment = False
    rev, shot, sGovernment = 0, 0, 0

    for i in range(11):
        l = l + ('fas',)
    for i in range(6):
        l = l + ('lib',)
    l = shuffle(l)

    print(l)
    print(players)
    print(roles)
    
    for i, player in enumerate(roles):
        if(player == 'fas'):
            fascists.append(players[i])
    hitler = 0
    for i, player in enumerate(roles):
        if(player == 'hit'):
            hitler = players[i]
    for i, player in enumerate(roles):
        if(player == 'lib'):
            liberals.append(players[i])
    await sendInformation(fascistNumber, hitler, fascists)

    president = players[random.randrange(0, len(players))]
    while(not end):
        if(len(l) < 3):
            for i in range(len(discard)):
                l = l + (discard.pop(),)
            l = shuffle(l)
        president, chancellor, chaos = await choseGovernment(president, players, lastPresident, lastChancellor,)
        if(await check(lib, fas, chancellor, roles, players, hitler)):
            end = True
            break
        if(chaos):
            if(l[0] == 'lib'):
                lib += 1
                l = l[1:]
        else:
            votingLaws = l[:3]
            l = l[3:]
            choosed = False
            while(not choosed):
                print(l)
                await send(president, l)
                print(','.join(votingLaws))
                await send(president, ','.join(votingLaws))
                print(president, ':Choose one you want to discard.')
                await send(president, 'Choose one you want to discard.')

                try:
                    while True:
                        input = int(await commands.get())
                        if input[1]==president:
                            break
                    inp=input[0]
                    if(inp > 0 and inp < 4):
                        discard.append(votingLaws[inp - 1])
                        votingLaws = votingLaws[:inp-1] + votingLaws[inp:]
                        choosed = True
                    else:
                        print(president, ':You must type number 1-3, which law you want to discard.')
                        await send(president, 'You must type number 1-3, which law you want to discard.')
                except:
                    print(president, ':You must type number 1-3, which law you want to discard.')
                    await send(president, 'You must type number 1-3, which law you want to discard.')
            choosed = False
            while(not choosed):
#                try:
                    print(','.join(votingLaws))
                    await send(chancellor, ','.join(votingLaws))
                    print(chancellor, ':Choose one you want to discard.')
                    await send(chancellor, 'Choose one you want to discard.')
                    
                    while True:
                        input = int(await commands.get())
                        if input[1]==chancellor:
                            break
                    inp=input[0]
                    discard.append(votingLaws[inp - 1])
                    votingLaws = votingLaws[:inp-1] + votingLaws[inp:]
                    if(votingLaws[0] == 'lib'):
                        lib +=1
                        print('Everyone: A liberal law was elected.')
                        await send('Everyone', 'A liberal law was elected.')
                    else:
                        fas +=1
                        print('Everyone: A fascist law was elected.')
                        await send('Everyone', 'A fascist law was elected.')
                        if((len(players) >= 9 and fas == 1 and rev < 1) or (len(players) >= 9 and fas == 2 and rev < 2)):
                            x = True
                            while(x):
                                print(president, ':Type the name of player, you want to reveal to you.')
                                await send(president, 'Type the name of player, you want to reveal to you.')
                                while True:
                                    input = int(await commands.get())
                                    if input[1]==president:
                                        break
                                inp=input[0]
                                if(inp in players):
                                    x = False
                            print(president, ':', inp, 'is', reveal(fascists, hitler, inp), '.')
                            await send(president, inp, 'is', reveal(fascists, hitler, inp), '.')
                            rev += 1
                        elif(len(players) >= 7 and fas == 2 and rev < 1):
                            x = True
                            while(x):
                                print(president, ':Type the name of player, you want to reveal to you.')
                                await send(president, 'Type the name of player, you want to reveal to you.')
                                while True:
                                    input = int(await commands.get())
                                    if input[1]==president:
                                        break
                                inp=input[0]
                                if(inp in players):
                                    x = False
                            print(president, ':', inp, 'is', reveal(fascists, hitler, inp), '.')
                            await send(president, inp, 'is', reveal(fascists, hitler, inp), '.')
                            rev += 1
                        elif(fas == 3 and sGovernment < 1):
                            specialGovernment = True
                            sGovernment += 1
                        elif((fas == 4 and shot < 1) or (fas == 5 and shot < 2)):
                            x = True
                            while(x):
                                print(president, ':Type the name of player, you want to kill.')
                                await send(president, 'Type the name of player, you want to kill.')
                                while True:
                                    input = int(await commands.get())
                                    if input[1]==president:
                                        break
                                inp=input[0]
                                if(inp in players and not (inp == president)):
                                    x = Falsel
                                if(inp == lastPresident):
                                    lastPresident = 0
                                elif(inp == lastChancellor):
                                    lastChancellor = 0
                            players, roles, end = kill(players, roles, hitler, inp)
                            shot += 1
                    choosed = True
#                except:
#                    print(chancellor,':You must type number 1 or 2, which law you want to discard.'
        if(specialGovernment):
            if(len(l) < 3):
                for i in range(len(discard)):
                    l = l + (discard.pop(),)
            l = shuffle(l)
            specialPresident = 0
            print(president, ':Who do you want as a president in special government?')
            await send(president, 'Who do you want as a president in special government?')
            x = True
            while(x):
                while True:
                    input = int(await commands.get())
                    if input[1]==president:
                        break
                inp=input[0]
                if(inp in players):
                    specialPresident = inp
                    x = False
                else:
                    print(president + ':You have to type the name of that player.')
                    await send(president, 'You have to type the name of that player.')
            chancellor = players[await choseChancellor(players, specialPresident, 0, 0)]
            if(await voting(players, president, chancellor) == True):
                
                votingLaws = l[:3]
                l = l[3:]
                choosed = False
                while(not choosed):
                    print(l)
                    await send(specialPresident,l)
                    print(','.join(votingLaws))
                    await send(specialPresident, ','.join(votingLaws))
                    print(specialPresident, ':Choose one you want to discard.')
                    await send(specialPresident, 'Choose one you want to discard.')
                    try:                    
                        while True:
                            input = int(await commands.get())
                            if input[1]==specialPresident:
                                break
                        inp=int(input[0])
                        if(inp > 0 and inp < 4):
                            discard.append(votingLaws[inp - 1])
                            votingLaws = votingLaws[:inp-1] + votingLaws[inp:]
                            choosed = True
                        else:
                            print(specialPresident, ':You must type number 1-3, which law you want to discard.')
                            await send(specialPresident, 'You must type number 1-3, which law you want to discard.')
                    except:
                        print(specialPresident, ':You must type number 1-3, which law you want to discard.')
                        await send(specialPresident, 'You must type number 1-3, which law you want to discard.')
                choosed = False
                while(not choosed):
    #                try:
                        print(','.join(votingLaws))
                        await send(chancellor, ','.join(votingLaws))
                        print(chancellor, ':Choose one you want to discard.')
                        await send(chancellor, 'Choose one you want to discard.')
                        while True:
                            input = int(await commands.get())
                            if input[1]==chancellor:
                                break
                        inp=int(input[0])
                        discard.append(votingLaws[inp - 1])
                        votingLaws = votingLaws[:inp-1] + votingLaws[inp:]
                        if(votingLaws[0] == 'lib'):
                            lib +=1
                            print('Everyone: A liberal law was elected.')
                            await send('Everyone', 'A liberal law was elected.')
                        else:
                            fas +=1
                            print('Everyone: A fascist law was elected.')
                            await send('Everyone', 'A fascist law was elected.')
                            if((fas == 4 and shot < 1) or (fas == 5 and shot < 2)):
                                x = True
                                while(x):
                                    print(specialPresident, ':Type the name of player, you want to kill.')
                                    await send(specialPresident, 'Type the name of player, you want to kill.')
                                    while True:
                                        input = int(await commands.get())
                                        if input[1]==specialPresident:
                                            break
                                    inp=input[0]
                                    if(inp in players and not (inp == specialPresident)):
                                        x = False
                                if(inp == president):
                                    president = players[(players.index(president) + len(players) - 1) % len(players)]
                                elif(inp == lastPresident):
                                    lastPresident = 0
                                elif(lastChancellor == inp):
                                    lastChancellor = 0
                                players, roles, end = kill(players, roles, hitler, inp)
                                shot += 1
                        choosed = True
    #                except:
    #                    print(chancellor,':You must type number 1 or 2, which law you want to discard.')
            specialGovernment = False
            lastPresident = specialPresident
            president, hugabuga, lastChancellor = nextpresident(players, president, chancellor)
            if(not(await check(lib, fas, chancellor, roles, players, hitler) == 0)):
                end = True
        else:
            president, lastPresident, lastChancellor = nextpresident(players, president, chancellor)
            if(not(check(lib, fas, chancellor, roles, players, hitler) == 0)):
                end = True


async def giveRoles(playerNumber):
    global roles
    for i in range(playerNumber):
        roles.append('lib')
    if(playerNumber == 5):
        roles[random.randrange(0, playerNumber)] = 'hit'
        c = 0
        while(c < 1):
            i = random.randrange(0, playerNumber)
            if(roles[i] == 'lib'):
                roles[i] = 'fas'
                c += 1
        return 2
    elif(playerNumber == 6):
        roles[random.randrange(0, playerNumber)] = 'hit'
        c = 0
        while(c < 1):
            i = random.randrange(0, playerNumber)
            if(roles[i] == 'lib'):
                roles[i] = 'fas'
                c += 1
        return 2
    elif(playerNumber == 7):
        roles[random.randrange(0, playerNumber)] = 'hit'
        c = 0
        while(c < 2):
            i = random.randrange(0, playerNumber)
            if(roles[i] == 'lib'):
                roles[i] = 'fas'
                c += 1
        return 3
    elif(playerNumber == 8):
        roles[random.randrange(0, playerNumber)] = 'hit'
        c = 0
        while(c < 2):
            i = random.randrange(0, playerNumber)
            if(roles[i] == 'lib'):
                roles[i] = 'fas'
                c += 1
        return 3
    elif(playerNumber == 9):
        roles[random.randrange(0, playerNumber)] = 'hit'
        c = 0
        while(c < 3):
            i = random.randrange(0, playerNumber)
            if(roles[i] == 'lib'):
                roles[i] = 'fas'
                c += 1
        return 4
    elif(playerNumber == 10):
        roles[random.randrange(0, playerNumber)] = 'hit'
        c = 0
        while(c < 3):
            i = random.randrange(0, playerNumber)
            if(roles[i] == 'lib'):
                roles[i] = 'fas'
                c += 1
        return 4
    else:
        print('Everyone: ' + 'There are too few or too many players. You must end the game.')
        await send('Everyone', 'There are too few or too many players. You must end the game.')

async def sendInformation(fascistNumber, hitler, fascists):
    global roles, players
    print("sending info")
    for i, player in enumerate(players):
        if(roles[i] == 'lib'):
            print(player, ':You are a LIBERAL. There are ', fascistNumber, ' fascists among the rest.')
            await send(player, 'You are a LIBERAL. There are ', fascistNumber, ' fascists among the rest.')
        elif(roles[i] == 'hit'):
            print(player, ':You are da HITLER. There are ', fascistNumber - 1, ' other fascists among the rest.')    
            await send(player, 'You are da HITLER. There are ', fascistNumber - 1, ' other fascists among the rest.')    
        elif(roles[i] == 'fas'):
            x = fascists.pop(0)
            if(fascistNumber == 3):
                print(player, ':You are a FASCIST. Your teammate is', fascists[0], '. ', hitler, 'is SECRET HITLER. Protect him and win.')
                await send(player, 'You are a FASCIST. Your teammate is', fascists[0], '. ', hitler, 'is SECRET HITLER. Protect him and win.')
                fascists.append(x)
            elif(fascistNumber == 4):
                print(player, ':You are a FASCIST. Your teammates are', ', '.join(fascists), '. ', players[roles.index(hitler)], 'is SECRET HITLER. Protect him and win.')
                await send(player, 'You are a FASCIST. Your teammates are', ', '.join(fascists), '. ', players[roles.index(hitler)], 'is SECRET HITLER. Protect him and win.')
                fascists.append(x)
            else:
                print(player, ':You are a FASCIST. There are no other fascists. ', players[roles.index(hitler)], ' is SECRET HITLER. Protect him and win.')
                await send(player, 'You are a FASCIST. There are no other fascists. ', players[roles.index(hitler)], ' is SECRET HITLER. Protect him and win.')

async def getvote(player):
    global hlasy
    print(player, 'Do you agree with goverment where the president would be', president, 'and the chancellor would be', chancellor)
    await send(player, 'Do you agree with goverment where the president would be', president, 'and the chancellor would be', chancellor)
    while True:
        input = int(await commands.get())
        if input[1]==p:
            break
    ans=input[0]
    if not ans[1] in hlasy:
        hlasy.append(ans[1])
        if(ans == 'ja'):
            return 1
        else:
            return 2

async def voting(players, president, chancellor):
    global lastVoting
    global hlasy
    for i in hlasy:
        hlasy.pop(0)
    ja, nein = 0, 0
    for i, p in enumerate(players):
        
        result = await getvote(p)
        if result == 1:
            ja += 1
        else:
            nein += 1
    if(ja > nein):
        lastVoting = True
        return True
    else:
        lastVoting = False
        return False

async def choseChancellor(players, president, lastPresident, lastChancellor):
    print(president, ':Who do you want as a chancellor in your government?')
    await send(president, 'Who do you want as a chancellor in your government?')
    while(True):
 #       if commands.empty():
  #          continue
        while True:
            input = int(await commands.get())
            if input[1]==president:
                break
        inp=input[0]

        if(inp == lastPresident):
            print(president, inp + 'can not be president, because he was president in last govenment.')
            await send(president, inp + 'can not be president, because he was president in last govenment.')
        elif(inp == lastChancellor):
            print(president, ': ', inp, 'can not be chancellor, because he was chancellor in last goverment.')
            await send(president, inp + 'can not be chancellor, because he was chancellor in last goverment.')
        elif(inp == president):
            print(president, ': ', inp, 'you can not be chancellor, you are already president.')
            await send(president, 'You can not be chancellor, you are already president.')
        elif(inp in players):
            return players.index(inp)
        else:
            print(president, ':You have to type the name of that player. ' + inp.content + ' is not in this list:') 
            print(players)
            await send(president, 'You have to type the name of that player.')

async def choseGovernment(president, players, lastPresident, lastChancellor):
    canceledVotings = 0
    while(True):
        chancellor = players[await choseChancellor(players, president, lastPresident, lastChancellor)]
        if(await voting(players, president, chancellor) == True):
            return president, chancellor, False
        else:
            canceledVotings += 1
            if(canceledVotings >= 3):
                return president, chancellor, True
            nextpresident(players, president, chancellor, lastPresident)
    
def nextpresident(players, president, chancellor):
    return players[(players.index(president) + 1) % len(players)], president, chancellor

def shuffle(a):
    x = []
    y = list(a)
    for i in range(len(y)):
        x.append(y.pop(random.randrange(0, len(y))))
    return tuple(x)

async def check(lib, fas, chancellor, roles, players, hitler):
    if(lib == 5):
        print('Everyone: Five liberal laws have been elected. Liberals win.')
        await send('Everyone', ' Five liberal laws have been elected. Liberals win.')
        return True
    elif(fas == 6):
        print('Everyone: Six fascistic laws have been elected. Fascists win.')
        await send('Everyone', ' Six fascistic laws have been elected. Fascists win.')
        return True
    elif(fas == 3 and roles[players.index(chancellor)] == 'hit'):
        print('Everyone: You choosed Hitler as a chancellor. Fascists win.')
        await send('Everyone', ' You choosed Hitler as a chancellor. Fascists win.')
        return True
    elif(not ('hit' in roles)):
        print('Everyone: Hitler was killed. Hitler was', hitler, ', liberals win.')
        await send('Everyone', ' Hitler was killed. Hitler was', hitler, ', liberals win.')
        return True
    else:
        return False

def reveal(fascists, hitler, name):
    if(name == hitler or name in fascists):
        return 'fascist'
    else:
        return 'liberal'

def kill(players, roles, hitler, name):
    del roles[players.index(name)]
    players.remove(name)
    return players, roles, hitler == name





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
