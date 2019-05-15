import discord
import random
import queue
import asyncio
import copy
import pyperclip
import sys
sys.path.append("D:\personal\matko\programovanie")
import statement as st
client = discord.Client()
kanale = []
hraci = []
roles = []
players = []
hlasy = []
creator=discord.member
running = False
commands = asyncio.Queue()
ready = False
global president
global chancellor
global lastPresident
global lastChancellor
game_in_progress = False
role_playing = discord.Role
role_creator = discord.Role

def refresh_kanalov():
	global role_playing
	print("refresh")
	global privatny
	for cech in client.guilds:
		print(cech)
		for kanal in cech.channels:
			kanale.append(kanal)
			print("kanal: " + kanal.name)

#			if kanal.name=="sukromne":
 #			   privatny = kanal
  #			  print(privatny)

@client.event
async def on_ready():
	global ready
	global role_playing
	global role_creator
	for cech in client.guilds:
		if cech.name=="Secret Kalab":
			role_playing = cech.get_role(570682937352388608)
			role_creator = cech.get_role(570689744338419712)

	print('We have logged in as {0.user}'.format(client))
	running=False
	ready = True
	refresh_kanalov()






@client.event
async def on_message(message):
	global running
	global game_in_progress
	global public_channel
	global privatny
	global ready
	global president
	global role_playing
	global role_creator
	if message.author == client.user:
		return

	if not ready:
		print("not reaady yet")
		return


	print(message.author.name)
	existuje_kanal = False
	for channel in kanale:
		if channel.name == message.author.name.lower():
			existuje_kanal = True
			break
	if not existuje_kanal:
#		await message.channel.send(message.author.name + ", you don't have private channel with me, named " + message.author.name.lower() + 
#		", so you won't be able to join any game, unless you create one :)")
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
					await message.author.add_roles(role_playing)
					await message.channel.send(message.author.name + " has just joined succesfully. There are " + str(len(hraci)) + " players joined.")
				else:
					await message.channel.send(message.author.name + " is already in the joined players list.")

	elif message.content == "$create":
		for clovek in message.guild.members:
			if role_playing in clovek.roles:
				await clovek.remove_roles(role_playing)
			if role_creator in clovek.roles:
				await clovek.remove_roles(role_creator)
		
		if running == False:
			for x in hraci:
				hraci.pop(0)
			public_channel=message.channel
			running = True
			await message.author.add_roles(role_playing)
			await message.author.add_roles(role_creator)
			await message.channel.send(message.author.name + " just created a game in this channel. Everyone can now join it!")
			hraci.append(message.author.name.lower())
		else:
			await message.channel.send("Game is already running.. wait for its end please")

	
	elif message.content == "$start":
		if len(hraci)>=5 and running and not game_in_progress and message.author in role_creator.members:
			global role_president
			global role_chancellor

			role_president = message.guild.get_role(570683158308192283)
			role_chancellor = message.guild.get_role(570683148480937984)

			await message.channel.send("Let the game... begin!")
			game_in_progress = True
			await play(hraci)
			
		else:
			await message.channel.send("Not enough players are joined :(. Looks like you have less than 5 friends.")


	elif message.content == "$delete":
		if message.author in role_creator.members:
			await message.channel.send("Well, game was just deleted..")
			running = False
		for clovek in message.guild.members:
			if role_playing in clovek.roles:
				await clovek.remove_roles(role_playing)
			if role_creator in clovek.roles:
				await clovek.remove_roles(role_creator)

	elif message.content == "$fill":
		if message.author.name != 'MvKal':
			return
		await message.author.send("Filled for you with dummies")
		dummici = ['a', 'b', 'c', 'd', 'e']
		for i in range(len(hraci), 5):
			print(i)
			hraci.append(dummici[i])
			for channel in kanale:
				if channel.name == dummici[i]:
					existuje_kanal = True
					break
			if not existuje_kanal:
#			   await message.channel.send(message.author.name + ", you don't have private channel with me, named " + message.author.name.lower() + 
#			   ", so you won't be able to join any game, unless you create one :)")
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

	elif message.content == "$data":
		print(players)
		print(commands)
		print(president)
		print(chancellor)

	elif message.content == "$help":
		print("helping....")
		await message.channel.send("hehe ask real kalab if you are that noob-ish")

	elif message.content.startswith("$decode"):
		optcode = []
		global base  
		base = st.Statement("start", 0, 1)
		code = message.content[8:]
		optcode = list(map(int, code.split()))
		create_statement_for(base, optcode)
		emb = discord.Embed (title = "MvKal")
		await message.channel.send(message.author.name + ": " + print_state(), tts = True, nonce = 5)
		await message.delete()

	else:
		if not game_in_progress:
			await message.channel.send("Sorry, I am now unable to commit " + message.content[1:])
		else:
			to_send=message.content[1:]
			print("putujem " + to_send + message.author.name.lower())
			await commands.put((to_send, message.author.name.lower()))


'''
TODO: 
oprotisediaci


'''


def create_statement_for(base, code = []):
	
	if len(base.pos_subs) == 0:
		return
	for which, subbie in enumerate(base.sub):
		print("Current state is:" + print_state())
		print("Possible values are:")
		if subbie.num_of_text != -1:
			continue
		max = 0
		try:
			for current_sub in base.pos_subs[which]:

				temp = st.Statement(current_sub)

				extended = False
				for num, pos in  enumerate (temp.text):
					temp.num_of_text = num
					print(str(max) +": " + temp.export())
					max += 1
				if temp.extendable:
					num += 1
					print(str(num) +": /empty/")
					max += 1
		except IndexError:
			print("bulshit")
		done = False
		while not done:
			if len(code)==0:
				inp = eval(input())
			else:
				inp = code[0]
				del code[0]
			try:
				inp = int(inp)
				if inp < max:
					if subbie.extendable and inp == max - 1:
						extended = True
						base.text2 = "nothing"
						base.input.append(inp)
						del base.pos_subs[-1]
					done = True
			except ValueError:
				done = False
		if not extended:
			base.input.append(inp)
			for txt in base.pos_subs[which]:
				temp = st.Statement(txt)
				if len(temp.text) <= inp:
					inp-= len(temp.text)
				else:
					temp.num_of_text = inp
					
					base.sub[which] = copy.deepcopy(temp)
					break
		if not extended:
			create_statement_for(base.sub[which], code)
	
				
def print_state():
	global base
	return base.export()

async def give_role(player, role):
	for srver in client.guilds:
		for clovek in srver.members:
			if clovek.name.lower == player:
				clovek.add_roles(role)

async def send(recepient, content, *texty):
	global public_channel
	sent = 0
	for text in texty:
		content = str(content) + str(text) + ' '
	print(str(recepient) + ": ")
	if recepient == "Everyone":
		await public_channel.send(content)
	for channel in kanale:
		if channel.name == recepient:
			print(content)
			await channel.send(content)
			sent+=1
	if sent == 0:
		print("chudak je bez channelu")

########################################################################################################################################################
async def vstup(authorized):
	while True:
		input = int(await commands.get())
		if input[1]==authorized:
			break
	inp=input[0]

async def play(gamers):
	global players
	global president
	global chancellor
	global lastPresident
	global lastChancellor
	players = gamers
	print("hrac 1 je : " + str(players[0]))
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
	hitler = 0
	for i, player in enumerate(roles):
		if(player == 'fas'):
			fascists.append(players[i])
		elif(player == 'hit'):
			hitler = players[i]
		elif(player == 'lib'):
			liberals.append(players[i])
		else:
			 raise Exception("heh, someone is undefined role")
	await sendInformation(fascistNumber, hitler, fascists)

	president = players[random.randrange(0, len(players))]
	await give_role(president, role_president)
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
					inp = await vstup(president)
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
#				try:
					print(','.join(votingLaws))
					await send(chancellor, ','.join(votingLaws))
					print(chancellor, ':Choose one you want to discard.')
					await send(chancellor, 'Choose one you want to discard.')
					
					inp = await vstup(chancellor)
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
								inp = await vstup(president)
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
								inp = await vstup(president)
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
								inp = await vstup(president)
								if(inp in players and not (inp == president)):
									x = Falsel
								if(inp == lastPresident):
									lastPresident = 0
								elif(inp == lastChancellor):
									lastChancellor = 0
							players, roles, end = kill(players, roles, hitler, inp)
							shot += 1
					choosed = True
#				except:
#					print(chancellor,':You must type number 1 or 2, which law you want to discard.'
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
				inp = await vstup(president)
				if(inp in players):
					specialPresident = inp
					await give_role(specialPresident, role_president)
					x = False
				else:
					print(president + ':You have to type the name of that player.')
					await send(president, 'You have to type the name of that player.')
			chancellor = players[await choseChancellor(players, specialPresident, 0, 0)]
			await give_role(chancellor, role_chancellor)
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
						inp = await vstup(specialPresident)
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
	#				try:
						print(','.join(votingLaws))
						await send(chancellor, ','.join(votingLaws))
						print(chancellor, ':Choose one you want to discard.')
						await send(chancellor, 'Choose one you want to discard.')
						inp = await vstup(chancellor)
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
									inp = await vstup(specialPresident)
									if(inp in players and not (inp == specialPresident)):
										x = False
								if(inp == president):
									president = players[(players.index(president) + len(players) - 1) % len(players)]
									await give_role(president, role_president)
								elif(inp == lastPresident):
									lastPresident = 0
								elif(lastChancellor == inp):
									lastChancellor = 0
								players, roles, end = kill(players, roles, hitler, inp)
								shot += 1
						choosed = True
	#				except:
	#					print(chancellor,':You must type number 1 or 2, which law you want to discard.')
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
	global roles
	global players
	print("sending info")
	i=0
	for player in players:
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
				print(player, ':You are a FASCIST. There are no other fascists. ', hitler, ' is SECRET HITLER. Protect him and win.')
				await send(player, 'You are a FASCIST. There are no other fascists. ', hitler, ' is SECRET HITLER. Protect him and win.')
		else:
			print("weird.. nic")
		i+=1

async def getvote():
	global hlasy

	input = await commands.get()

	ans=input[0]
	if (not ans[1] in hlasy) and (ans[1] in players):
		hlasy.append(ans[1])
		if(ans == 'ja'):
			return 1
		elif (ans == 'nein'):
			return 2

async def voting(players, president, chancellor):
	global lastVoting
	global hlasy

	global lastPresident
	global lastChancellor
	resulty = []
	for i in hlasy:
		hlasy.pop(0)
	ja, nein = 0, 0
	for i, p in enumerate(players):
		print(p, 'Do you agree with goverment where the president would be ', president, 'and the chancellor would be', chancellor)
		await send(p, 'Do you agree with goverment where the president would be ', president, 'and the chancellor would be', chancellor)

	for p in players:
		resulty.append(await getvote())

	while len(resulty)<len(players):
		await sleep(1)

	for i, p in enumerate(players):
		if resulty[i] == 1:
			ja += 1
		else:
			nein += 1
		print("Ja: " + str(ja) + ", Nein: " + str(nein))
		print("hlasovali: ")
		print(hlasy)

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
 #	   if commands.empty():
  #		  continue
		inp = await vstup(president)

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

	global chancellor

	canceledVotings = 0
	while(True):
		chancellor = players[await choseChancellor(players, president, lastPresident, lastChancellor)]
		await give_role(chancellor, role_chancellor)
		if(await voting(players, president, chancellor) == True):
			return president, chancellor, False
		else:
			canceledVotings += 1
			if(canceledVotings >= 3):
				return president, chancellor, True
			choseGoverment(players, (nextpresident(players, president, chancellor))[0], lastPresident, lastChancellor)
	
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





client.run()


'''	if existuje_kanal==False:
		print(server)
		over ={
		discord.Guild.default_role: discord.PermissionOverwrite(read_messages=True),
		discord.Guild.me: discord.PermissionOverwrite(read_messages=True)
		}
		novy = discord.abc.GuildChannel()
		await server.create_text_channel(server, "mvkal", overwrites = over, category="sukromne")
		kanale.append(novy)
#		await kanale[len(kanale)-1].send(None)
#		await kanale[len(kanale)-1].send("i WORK")
		print(kanale[len(kanale)-1])'''
