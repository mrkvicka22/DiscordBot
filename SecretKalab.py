import discord
import random
import queue
import asyncio
import copy
import winsound
import string
import sys
import os

sys.path.append("D:\personal\matko\programovanie")
import statement as st
import numpy as np
from aioconsole import ainput
client = discord.Client()
kanale = []
hraci = []
roles = []
players = []
hlasy = []
ai_players = []
creator = discord.member
running = False
commands = asyncio.Queue()
ready = False
global president
global chancellor
global lastPresident
global lastChancellor
illegal_action_punishment = -3
game_in_progress = False
role_playing = discord.Role
role_creator = discord.Role
history = []
turnhiskeys = ['president', 'chancellor', 'voting laws', 'president discarded', 'chancellor discarded']
turnhis = []
runtype = "ai_train"
random_ai = True
if runtype == "ai_train":
	print("importing TS...")
	import tensorflow as tf
	from tensorflow import keras
	from keras.models import model_from_json



print("importing done")


class AI_player:
	global public

	def __init__(self, name, party, ** pWeights):
		public = np.zeros(24)
		self.personal_inputs = np.zeros(32)
		self.fitness = 0
		self.party = party
		self.name = name
		self.networks = {
			"vote":
				keras.Sequential([
					keras.layers.Dense((len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(1, activation=tf.nn.softmax)
				]),
			"choose_chancellor":
				keras.Sequential([
					keras.layers.Dense((len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(4, activation=tf.nn.softmax)
				]),
			"shoot":
				keras.Sequential([
					keras.layers.Dense((len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(4, activation=tf.nn.softmax)
				]),
			"passing laws":
				keras.Sequential([
					keras.layers.Dense((3 + len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(1, activation=tf.nn.softmax)
				]),
			"investigate":
				keras.Sequential([
					keras.layers.Dense((len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(4, activation=tf.nn.softmax)
				]),
			"special-elect":
				keras.Sequential([
					keras.layers.Dense((len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(4, activation=tf.nn.softmax)
				]),
			"public info update":
				keras.Sequential([
					keras.layers.Dense((len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(len(self.personal_inputs), activation=tf.nn.tanh)
				]),
			"punishment":
				keras.Sequential([
					keras.layers.Dense((len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(len(self.personal_inputs), activation=tf.nn.tanh)
				]),
			"investigate claim":
				keras.Sequential([
					keras.layers.Dense((len(self.personal_inputs) + len(public))),
					keras.layers.Dense(len(self.personal_inputs) + len(public), activation=tf.nn.tanh),
					keras.layers.Dense(1, activation=tf.nn.softmax)
				])
		}
		# print(self.networks["choose_chancellor"].input_shape)

		for network in self.networks:
			for w in self.networks[network].weights:
				if len(pWeights)>0:
					w = pWeights[0]
					pWeights.pop()
				else:
					w = random.random()

	def mutate(self, amp):
		weights = []
		for network in self.networks:
			weights.append(self.networks[network].get_weights.tolist())
			#for w in self.networks[network].weights:
				#weights.append(w)

		for x in range(0, int(random.random() * amp * len(weights))):
			weights[random.randrange(0, len(weights))] = weights[random.randrange(0, len(
				weights))] - 0.001 + 0.001 * random.random() * 2

	def give_weights(self):
		out = []
		for type in self.networks:
			out.append(self.networks[type].weights)
		print(out)
		return out


	def give_answer(self, event_type, optinputs=np.array([])):
		global random_ai
		inp = np.array([np.concatenate((self.personal_inputs, public, optinputs))])
		print(event_type)
		# print(inp.shape)
		if not random_ai:
			raw_out = self.networks[event_type].predict(inp)
			out = raw_out[0].tolist()
		else:
			out = [random.random()-0.5, random.random()-0.5, random.random()-0.5, random.random()-0.5]
		if event_type == "vote":
			if out[0] > 0:
				ret = "ja"
			else:
				ret = "nein"
		elif event_type == "passing laws":
			laws = []
			for l in optinputs:
				laws.append(int(l))
			if out[0] >= 0:
				ret = laws.index(1) + 1
			else:
				ret = laws.index(-1) + 1

		elif event_type == "investigate claim":
			if out[0] > 0:
				ret = "lib"
			else:
				ret = "fas"
		elif event_type == ("public info update" or event_type == "punishment") and not random_ai:
			self.personal_inputs = raw_out[0]
			return
		else:
			ret = players[(out.index(max(out)) + players.index(self.name) + 1) % len(players)]
		print("NN out: ")
		print(ret)
		return ret

	def save_models_to_json(self):
		# serialize model to JSON
		for model in self.networks:
			json_path = os.path.join("model saves", self.party, self.name + "_model_+" + model + ".json")
			h5_path = os.path.join("model saves", self.party, self.name + "_model_+" + model + ".h5")
			model_json = self.networks[model].to_json()
			with open(json_path, "w") as json_file:
				json_file.write(model_json)
			# serialize weights to HDF5
			self.networks[model].save_weights(h5_path)
			print("Saved model "+model+" to disk with name " + self.name)

	def load_models_from_json(self):
		# load json and create model
		for model in self.networks:
			json_path = os.path.join("model saves", self.party, self.name + "_model_+" + model + ".json")
			h5_path = os.path.join("model saves", self.party, self.name + "_model_+" + model + ".h5")
			json_file = open(json_path, 'r')
			loaded_model_json = json_file.read()
			json_file.close()
			loaded_model = model_from_json(loaded_model_json)
			# load weights into new model
			loaded_model.load_weights(h5_path)
			print("Loaded model "+model+" from disk")

def refresh_kanalov():
	global role_playing
	print("refresh")
	global privatny
	for cech in client.guilds:
		#print(cech)
		for kanal in cech.channels:
			kanale.append(kanal)
			#print("kanal: " + kanal.name)


#			if kanal.name=="sukromne":
#			   privatny = kanal
#			  print(privatny)

@client.event
async def on_ready():
	global ready
	global role_playing
	global role_creator
	for cech in client.guilds:
		if cech.name == "Secret Kalab":
			role_playing = cech.get_role(570682937352388608)
			role_creator = cech.get_role(570689744338419712)

	print('We have logged in as {0.user}'.format(client))
	running = False
	ready = True
	refresh_kanalov()
	await console_input()


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
	global players
	delet = True
	if message.author == client.user:
		return

	if not ready:
		print("not reaady yet")
		return

	print(message.author.name + ": " + message.content)
	existuje_kanal = False
	refresh_kanalov()
	for channel in kanale:
		if channel.name == message.author.name.lower().replace(" ", ""):
			existuje_kanal = True
			await channel.purge()
			break
	if not existuje_kanal:
		#		await message.channel.send(message.author.name + ", you don't have private channel with me, named " + message.author.name.lower() +
		#		", so you won't be able to join any game, unless you create one :)")
		overwrites = {
			message.channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
			message.channel.guild.me: discord.PermissionOverwrite(read_messages=True),
			message.author: discord.PermissionOverwrite(read_messages=True)
		}

		# await server.create_text_channel('secret', overwrites=overwrites)
		novy = await message.guild.create_text_channel(message.author.name.lower().replace(" ", ""), overwrites=overwrites)
		# novy = client.start_private_message(message.author)
		await novy.send("hello here, here you will get your personal info you can't share")


	if not message.content.startswith('$'):
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')


	elif message.content == "$join":
		if running:
			if message.channel == public_channel:
				if not message.author.name.lower() in hraci:
					hraci.append(message.author.name.lower())
					await message.author.add_roles(role_playing)
					await message.channel.send(message.author.name + " has just joined succesfully. There are " + str(
						len(hraci)) + " players joined.")
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
			public_channel = message.channel
			running = True
			await message.author.add_roles(role_playing)
			await message.author.add_roles(role_creator)
			await message.channel.send(
				message.author.name + " just created a game in this channel. Everyone can now join it!")
			hraci.append(message.author.name.lower())
		else:
			await message.channel.send("Game is already running.. wait for its end please")


	elif message.content == "$start":
		if len(hraci) >= 5 and running and not game_in_progress and message.author in role_creator.members:
			global role_president
			global role_chancellor

			role_president = message.guild.get_role(570683158308192283)
			role_chancellor = message.guild.get_role(570683148480937984)

			await message.channel.send("Let the game... begin!")
			game_in_progress = True
			players = hraci
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

				# await server.create_text_channel('secret', overwrites=overwrites)
				novy = await message.guild.create_text_channel(i, overwrites=overwrites)
				# novy = client.start_private_message(message.author)
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
		emb = discord.Embed(title="MvKal")
		await message.channel.send(message.author.name + ": " + print_state(), tts=True, nonce=5)


	else:
		if not game_in_progress:
			await message.channel.send("Sorry, I am now unable to commit " + message.content[1:])
		else:
			if len(message.mentions) > 0:
				to_send = message.mentions[0].name.lower()
				delet = False
			else:
				to_send = message.content[1:]
			print("putujem " + to_send + message.author.name.lower())
			await commands.put((to_send, message.author.name.lower()))
	if delet:
		await message.delete()


'''
TODO: 
oprotisediaci


'''


def create_statement_for(base, code=[]):
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
				for num, pos in enumerate(temp.text):
					temp.num_of_text = num
					print(str(max) + ": " + temp.export())
					max += 1
				if temp.extendable:
					num += 1
					print(str(num) + ": /empty/")
					max += 1
		except IndexError:
			print("bulshit")
		done = False
		while not done:
			if len(code) == 0:
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
					inp -= len(temp.text)
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


async def set_public(group, index):
	global players
	global public
	if group < 4:
		for i in range(0, len(players)):
			public[i + len(players) * group] = 0
			if i == index:
				public[i + len(players) * group] = 1
	else:
		public[20+group-1] = index
	for ai in players:
		await vstup(ai, call_type="public info update")


async def send(recepient, content, *texty):
	global public_channel
	if runtype == "discord":
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
				sent += 1
		if sent == 0:
			print("chudak je bez channelu")


#	elif runtype == "ai_train":
#		if

########################################################################################################################################################
async def vstup(authorized, call_type=None, inputs=np.array([])):
	global ai_players
	if runtype == "discord":
		while True:
			input = await commands.get()
			print("nacital som " + input[0])
			if input[1] == authorized or input[1] == "mvkal":
				break
		inp = input[0]
		return inp
	elif runtype == "ai_train":
		try:
			for i in range(len(inputs)):
				if inputs[i] == "lib":
					inputs[i] = 1
				elif inputs[i] == "fas":
					inputs[i] = -1
		except ValueError:
			print("no additional inputs to NN")

		return ai_players[players.index(authorized)].give_answer(call_type, optinputs=inputs)


async def PUNISH(ind):
	global errors
	global players
	global ai_players
	if runtype == "ai_train":
		ai_players[ind].fitness += illegal_action_punishment
		await vstup(players[ind], call_type="punishment")
		errors -= 1
		if errors == 0:
			return True
		return False

async def console_input():
	while True:
		inp = await ainput(">>> ")
		if inp.startswith("pause"):
			input()

async def play(gamers):
	global players
	global president
	global chancellor
	global lastPresident
	global lastChancellor
	global ai_players
	global public
	global illegal_action_punishment
	global errors

	chancellor = None
	lastPresident = None
	lastChancellor = None
	public = np.zeros(24)  # 5-isPresident, isChancellor, lastPresident, lastChancellor
	# 1-fas_laws, lib_laws, TD in x, isHZ


	l = ()
	discard = []
	lib, fas = 0, 0
	global roles
	fascists, liberals = [], []
	if runtype == "discord": fascistNumber = await giveRoles(len(players))
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
	if runtype == "discord":
		for i, player in enumerate(roles):
			if (player == 'fas'):
				fascists.append(players[i])
			elif (player == 'hit'):
				hitler = players[i]
			elif (player == 'lib'):
				liberals.append(players[i])
			else:
				raise Exception("heh, someone is undefined role")
		await sendInformation(fascistNumber, hitler, fascists)
	elif runtype == "ai_train":
		for i, player in enumerate(ai_players):
			roles.append(player.party[:3])
			if player.party == "liberal":
				liberals.append(players[i])
			elif player.party == "fascist":
				fascists.append(players[i])
			elif player.party == "hitler":
				hitler = players[i]

	president = players[random.randrange(0, len(players))]

	if runtype == "discord":
		await give_role(president, role_president)
	await set_public(1, players.index(president))
	while (not end):
		errors = 25
		if (len(l) < 3):
			for i in range(len(discard)):
				l = l + (discard.pop(),)
			l = shuffle(l)
		await set_public(3, players.index(president))
		try:
			await set_public(4, players.index(chancellor))
		except ValueError:
			print("no last chancellor")
		president, chancellor, chaos = await choseGovernment(president, players, lastPresident, lastChancellor)
		# pridavam prezidenta a kancla do turn history
		turnhis.append(president)
		turnhis.append(chancellor)
		await set_public(1, players.index(president))
		await set_public(2, players.index(chancellor))
		if (await check(lib, fas, chancellor, roles, players, hitler)):
			end = True
			break
		if (chaos):
			if (l[0] == 'lib'):
				lib += 1
				l = l[1:]
			elif l[0] == "fas":
				fas += 1
				l = l[1:]
		else:
			votingLaws = l[:3]
			l = l[3:]
			choosed = False
			errors = 10
			while (not choosed):

				print(l)
				print(','.join(votingLaws))
				await send(president, ','.join(votingLaws))
				print(president, ':Choose one you want to discard.')
				await send(president, 'Choose one you want to discard.')

				try:
					try:
						inp = int(await vstup(president, call_type="passing laws", inputs=np.array(votingLaws)))
					except ValueError:
						send(president, "This was not a number")
						print("This was not a number")
						if await PUNISH(players.index(president)): return
					if (inp > 0 and inp < 4):
						presdisc = votingLaws[inp - 1]
						discard.append(presdisc)
						turnhis.append(votingLaws)

						discard.append(votingLaws[inp - 1])
						votingLaws = votingLaws[:inp - 1] + votingLaws[inp:]
						choosed = True
					else:
						print(president, ':You must type number 1-3, which law you want to discard.')
						await send(president, 'You must type number 1-3, which law you want to discard.')
						PUNISH(players.index(president))
				except:
					print(president, ':You must type number 1-3, which law you want to discard.')
					await send(president, 'You must type number 1-3, which law you want to discard.')
					PUNISH(players.index(president))
			choosed = False
			while (not choosed):
				try:
					print(','.join(votingLaws))
					await send(chancellor, ','.join(votingLaws))
					print(chancellor, ':Choose one you want to discard.')
					await send(chancellor, 'Choose one you want to discard.')

					inp = await vstup(chancellor, call_type="passing laws", inputs=np.array(votingLaws))
					discard.append(votingLaws[inp - 1])
					turnhis.append(votingLaws[inp - 1])
					history.append(dict(zip(turnhiskeys, turnhis)))
					votingLaws = votingLaws[:inp - 1] + votingLaws[inp:]
					if (votingLaws[0] == 'lib'):
						lib += 1
						print('Everyone: A liberal law was elected.')
						await send('Everyone', 'A liberal law was elected.')
					else:
						fas += 1
						print('Everyone: A fascist law was elected.')
						await send('Everyone', 'A fascist law was elected.')
						if ((len(players) >= 9 and fas == 1 and rev < 1) or (
								len(players) >= 9 and fas == 2 and rev < 2)):
							x = True
							while (x):
								print(president, ':Type the name of player, you want to reveal to you.')
								await send(president, 'Type the name of player, you want to reveal to you.')
								inp = await vstup(president, call_type="investigate")
								if (inp in players):
									x = False
							print(president, ':', inp, 'is', reveal(fascists, hitler, inp), '.')
							await send(president, inp, 'is', reveal(fascists, hitler, inp), '.')
							rev += 1
						elif (len(players) >= 7 and fas == 2 and rev < 1):
							x = True
							while (x):
								print(president, ':Type the name of player, you want to reveal to you.')
								await send(president, 'Type the name of player, you want to reveal to you.')
								inp = await vstup(president, call_type="investigate")
								if (inp in players):
									x = False
							print(president, ':', inp, 'is', reveal(fascists, hitler, inp), '.')
							await send(president, inp, 'is', reveal(fascists, hitler, inp), '.')
							rev += 1
						elif (fas == 3 and sGovernment < 1):
							specialGovernment = True
							sGovernment += 1
						elif ((fas == 4 and shot < 1) or (fas == 5 and shot < 2)):
							x = True
							while (x):
								print(president, ':Type the name of player, you want to kill.')
								await send(president, 'Type the name of player, you want to kill.')
								inp = await vstup(president, call_type="shoot")
								if (inp in players and not (inp == president)):
									x = False
								if (inp == lastPresident):
									lastPresident = 0
								elif (inp == lastChancellor):
									lastChancellor = 0
							players, roles, end = kill(players, roles, hitler, inp)
							shot += 1
					choosed = True
				except:
					print(chancellor, ':You must type number 1 or 2, which law you want to discard.')
					if await PUNISH(players.index(chancellor)): return
		if (specialGovernment):
			if (len(l) < 3):
				for i in range(len(discard)):
					l = l + (discard.pop(),)
			l = shuffle(l)
			specialPresident = 0
			print(president, ':Who do you want as a president in special government?')
			await send(president, 'Who do you want as a president in special government?')
			x = True
			while (x):
				inp = await vstup(president, call_type="special-elect")
				if (inp in players):
					specialPresident = inp
					await give_role(specialPresident, role_president)
					x = False
				else:
					print(president + ':You have to type the name of that player.')
					await send(president, 'You have to type the name of that player.')
					if await PUNISH(players.index(president)): return
			chancellor = players[await choseChancellor(players, specialPresident, 0, 0)]
			await give_role(chancellor, role_chancellor)
			if (await voting(players, president, chancellor) == True):

				votingLaws = l[:3]
				l = l[3:]
				choosed = False
				while (not choosed):
					print(l)
					await send(specialPresident, l)
					print(','.join(votingLaws))
					await send(specialPresident, ','.join(votingLaws))
					print(specialPresident, ':Choose one you want to discard.')
					await send(specialPresident, 'Choose one you want to discard.')
					try:
						inp = await vstup(specialPresident, call_type="passing laws", inputs=np.array(votingLaws))
						if (inp > 0 and inp < 4):
							discard.append(votingLaws[inp - 1])
							votingLaws = votingLaws[:inp - 1] + votingLaws[inp:]
							choosed = True
						else:
							print(specialPresident, ':You must type number 1-3, which law you want to discard.')
							await send(specialPresident, 'You must type number 1-3, which law you want to discard.')
							if await PUNISH(players.index(specialPresident)): return
					except:
						print(specialPresident, ':You must type number 1-3, which law you want to discard.')
						await send(specialPresident, 'You must type number 1-3, which law you want to discard.')
						if await PUNISH(players.index(specialPresident)): return
				choosed = False
				while (not choosed):
					try:
						print(','.join(votingLaws))
						await send(chancellor, ','.join(votingLaws))
						print(chancellor, ':Choose one you want to discard.')
						await send(chancellor, 'Choose one you want to discard.')
						inp = await vstup(chancellor, call_type="passing laws", inputs=np.array(votingLaws))
						discard.append(votingLaws[inp - 1])
						votingLaws = votingLaws[:inp - 1] + votingLaws[inp:]
						if (votingLaws[0] == 'lib'):
							lib += 1
							print('Everyone: A liberal law was elected.')
							await send('Everyone', 'A liberal law was elected.')
						else:
							fas += 1
							print('Everyone: A fascist law was elected.')
							await send('Everyone', 'A fascist law was elected.')
							if ((fas == 4 and shot < 1) or (fas == 5 and shot < 2)):
								x = True
								while (x):
									print(specialPresident, ':Type the name of player, you want to kill.')
									await send(specialPresident, 'Type the name of player, you want to kill.')
									inp = await vstup(specialPresident, call_type="shoot")
									if (inp in players and not (inp == specialPresident)):
										x = False
								if (inp == president):
									president = players[(players.index(president) + len(players) - 1) % len(players)]
									await give_role(president, role_president)
								elif (inp == lastPresident):
									lastPresident = 0
								elif (lastChancellor == inp):
									lastChancellor = 0
								players, roles, end = kill(players, roles, hitler, inp)
								shot += 1
						choosed = True
					except:
						print(chancellor, ':You must type number 1 or 2, which law you want to discard.')
						if await PUNISH(players.index(chancellor)): return
			specialGovernment = False
			lastPresident = specialPresident
			president, hugabuga, lastChancellor = nextpresident(players, president, chancellor)
			if (not (await check(lib, fas, chancellor, roles, players, hitler) == 0)):
				end = True
		else:
			president, lastPresident, lastChancellor = nextpresident(players, president, chancellor)
			if (not (await check(lib, fas, chancellor, roles, players, hitler) == 0)):
				end = True


async def giveRoles(playerNumber):
	global roles
	for i in range(playerNumber):
		roles.append('lib')
	if (playerNumber == 5):
		roles[random.randrange(0, playerNumber)] = 'hit'
		c = 0
		while (c < 1):
			i = random.randrange(0, playerNumber)
			if (roles[i] == 'lib'):
				roles[i] = 'fas'
				c += 1
		return 2
	elif (playerNumber == 6):
		roles[random.randrange(0, playerNumber)] = 'hit'
		c = 0
		while (c < 1):
			i = random.randrange(0, playerNumber)
			if (roles[i] == 'lib'):
				roles[i] = 'fas'
				c += 1
		return 2
	elif (playerNumber == 7):
		roles[random.randrange(0, playerNumber)] = 'hit'
		c = 0
		while (c < 2):
			i = random.randrange(0, playerNumber)
			if (roles[i] == 'lib'):
				roles[i] = 'fas'
				c += 1
		return 3
	elif (playerNumber == 8):
		roles[random.randrange(0, playerNumber)] = 'hit'
		c = 0
		while (c < 2):
			i = random.randrange(0, playerNumber)
			if (roles[i] == 'lib'):
				roles[i] = 'fas'
				c += 1
		return 3
	elif (playerNumber == 9):
		roles[random.randrange(0, playerNumber)] = 'hit'
		c = 0
		while (c < 3):
			i = random.randrange(0, playerNumber)
			if (roles[i] == 'lib'):
				roles[i] = 'fas'
				c += 1
		return 4
	elif (playerNumber == 10):
		roles[random.randrange(0, playerNumber)] = 'hit'
		c = 0
		while (c < 3):
			i = random.randrange(0, playerNumber)
			if (roles[i] == 'lib'):
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
	i = 0
	for player in players:
		if (roles[i] == 'lib'):
			print(player, ':You are a LIBERAL. There are ', fascistNumber, ' fascists among the rest.')
			await send(player, 'You are a LIBERAL. There are ', fascistNumber, ' fascists among the rest.')
		elif (roles[i] == 'hit'):
			print(player, ':You are da HITLER. There are ', fascistNumber - 1, ' other fascists among the rest.')
			await send(player, 'You are da HITLER. There are ', fascistNumber - 1, ' other fascists among the rest.')
		elif (roles[i] == 'fas'):
			x = fascists.pop(0)
			if (fascistNumber == 3):
				print(player, ':You are a FASCIST. Your teammate is', fascists[0], '. ', hitler,
					  'is SECRET HITLER. Protect him and win.')
				await send(player, 'You are a FASCIST. Your teammate is', fascists[0], '. ', hitler,
						   'is SECRET HITLER. Protect him and win.')
				fascists.append(x)
			elif (fascistNumber == 4):
				print(player, ':You are a FASCIST. Your teammates are', ', '.join(fascists), '. ',
					  players[roles.index(hitler)], 'is SECRET HITLER. Protect him and win.')
				await send(player, 'You are a FASCIST. Your teammates are', ', '.join(fascists), '. ',
						   players[roles.index(hitler)], 'is SECRET HITLER. Protect him and win.')
				fascists.append(x)
			else:
				print(player, ':You are a FASCIST. There are no other fascists. ', hitler,
					  ' is SECRET HITLER. Protect him and win.')
				await send(player, 'You are a FASCIST. There are no other fascists. ', hitler,
						   ' is SECRET HITLER. Protect him and win.')
		else:
			print("weird.. nic")
		i += 1


async def getvote():
	global hlasy

	input = await commands.get()

	ans = input[0]
	if (not (input[1] in hlasy)) and (input[1] in players):
		hlasy.append(input[1])
		if ans.lower() == 'ja' or ans.lower() == "nein":
			return ans.lower()


async def voting(players, president, chancellor):
	global lastVoting
	global hlasy

	global lastPresident
	global lastChancellor
	resulty = []
	ja, nein = 0, 0
	if runtype == "discord":
		for i in hlasy:
			hlasy.pop(0)

		for i, p in enumerate(players):
			print(p, 'Do you agree with goverment where the president would be ', president,
				  'and the chancellor would be', chancellor)
			await send(p, 'Do you agree with goverment where the president would be ', president,
					   'and the chancellor would be', chancellor)
			await send("Everyone", 'Do you agree with goverment where the president would be ', president,
					   'and the chancellor would be' + chancellor)

		for p in players:
			resulty.append(await getvote())
	elif runtype == "ai_train":
		for ai in players:
			resulty.append(await vstup(ai, call_type="vote"))

	while len(resulty) < len(players):
		await sleep(1)
	for i, p in enumerate(players):
		if resulty[i].lower() == "ja":
			ja += 1
		elif resulty[i].lower() == "nein":
			nein += 1
		else:
			raise Exception("Wrong input, can be 'ja' or 'nein', got " + resulty[i].lower())
		print("Ja: " + str(ja) + ", Nein: " + str(nein))
		print("hlasovali: ")
		print(hlasy)
	if (ja > nein):
		lastVoting = True
		return True
	else:
		lastVoting = False
		return False


async def choseChancellor(players, president, lastPresident, lastChancellor):
	global ai_players
	global illegal_action_punishment
	print(president, ':Who do you want as a chancellor in your government?')
	await send(president, 'Who do you want as a chancellor in your government?')
	while (True):
		inp = await vstup(president, call_type="choose_chancellor")
		if runtype == "ai_train": ai_players[players.index(president)].fitness += illegal_action_punishment
		if (inp == lastPresident):
			print(president, inp + 'can not be president, because he was president in last govenment.')
			await send(president, inp + 'can not be president, because he was president in last govenment.')
			if await PUNISH(players.index(president)): return
		elif (inp == lastChancellor):
			print(president, ': ', inp, 'can not be chancellor, because he was chancellor in last goverment.')
			await send(president, inp + 'can not be chancellor, because he was chancellor in last goverment.')
			if await PUNISH(players.index(president)): return
		elif (inp == president):
			print(president, ': ', inp, 'you can not be chancellor, you are already president.')
			await send(president, 'You can not be chancellor, you are already president.')
			if await PUNISH(players.index(president)): return
		elif (inp in players):
			if runtype == "ai_train": ai_players[players.index(president)].fitness -= illegal_action_punishment
			if players.index(inp) is None:
				print("NONETYPE ERROR")
			return players.index(inp)
		else:
			print(president, ':You have to type the name of that player. ' + inp + ' is not in this list:')
			await send(president, 'You have to type the name of that player.')
			if await PUNISH(players.index(president)): return


async def choseGovernment(president, players, lastPresident, lastChancellor):
	global chancellor
	global runtype
	global public
	canceledVotings = 0
	while (True):
		
		chancellor = players[await choseChancellor(players, president, lastPresident, lastChancellor)]
		
		if runtype == "discord": await give_role(chancellor, role_chancellor)
		print(chancellor)
		await set_public(2, players.index(chancellor))
		if (await voting(players, president, chancellor) == True):
			return president, chancellor, False
		else:
			canceledVotings += 1
			if (canceledVotings >= 3):
				return president, chancellor, True
			await choseGovernment(players, (nextpresident(players, president, chancellor))[0], lastPresident, lastChancellor)


def nextpresident(players, president, chancellor):
	return players[(players.index(president) + 1) % len(players)], president, chancellor


def shuffle(a):
	x = []
	y = list(a)
	for i in range(len(y)):
		x.append(y.pop(random.randrange(0, len(y))))
	return tuple(x)


async def check(lib, fas, chancellor, roles, players, hitler):
	if (lib == 5):
		print('Everyone: Five liberal laws have been elected. Liberals win.')
		await send('Everyone', ' Five liberal laws have been elected. Liberals win.')
		return True
	elif (fas == 6):
		print('Everyone: Six fascistic laws have been elected. Fascists win.')
		await send('Everyone', ' Six fascistic laws have been elected. Fascists win.')
		return True
	elif (fas == 3 and roles[players.index(chancellor)] == 'hit'):
		print('Everyone: You choosed Hitler as a chancellor. Fascists win.')
		await send('Everyone', ' You choosed Hitler as a chancellor. Fascists win.')
		return True
	elif (not ('hit' in roles)):
		print('Everyone: Hitler was killed. Hitler was', hitler, ', liberals win.')
		await send('Everyone', ' Hitler was killed. Hitler was', hitler, ', liberals win.')
		return True
	else:
		return False


def reveal(fascists, hitler, name):
	if (name == hitler or name in fascists):
		return 'fascist'
	else:
		return 'liberal'


def kill(players, roles, hitler, name):
	del roles[players.index(name)]
	players.remove(name)
	return players, roles, hitler == name


async def train():
	global ai_players
	global players
	global ai_bases
	num_of_players = 5
	configuration = [2, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1]
	ai_bases = {
		"lib_players": [],
		"fas_players": [],
		"hit_players": []
	}
	used_ais = {
		"lib_players": [],
		"fas_players": [],
		"hit_players": []
	}
	randmax = 100000
	generation_size_coef = 2
	generations_planned = 20
	mutation_chance = 0.2
	mutation_amplificator = 0.00001

#	for aip in lib_players:
#		aip.load_models_to_json()
#	for aip in fas_players:
#		aip.load_models_to_json()

	for i, type in enumerate(ai_bases):
		if i == 0:
			team = "liberal"
		elif i == 1:
			team = "fascist"
		else:
			team = "hitler"
		for j in range(configuration[:num_of_players].count(i) * generation_size_coef - len(ai_bases[type])):
			ai_bases[type].append(AI_player(''.join(random.choice(string.ascii_lowercase) for i in range(16)), team))
			
		


	for generation in range(0, generations_planned):
		rulette = []
		for typ in used_ais:
			used_ais[typ] = []
		

		for cycle in range(generation_size_coef):
			ai_players = []
			for i, type in enumerate(ai_bases):

				for j in range(configuration[:num_of_players].count(i)):
					x = random.randrange(0, len(ai_bases[type]))
					ai_players.append(ai_bases[type][x])
					used_ais[type].append(ai_bases[type][x])
					del ai_bases[type][x]
			random.shuffle(ai_players)
			players = [ai.name for ai in ai_players]
			print(players)
			await asyncio.wait_for(play(players), 30)
		#ai_bases = used_ais
		
		for i, type in enumerate(ai_bases):
			rulette = []
			addition = min([player.fitness for player in used_ais[type]])
			if addition >= 1:
				addition = 0
			else:
				addition = addition * -1 + 1
			for z, plai in enumerate(used_ais[type]):
				for fit in range(0, plai.fitness + addition):
					rulette.append(z)
			ai_bases[type] = []
			for pl in range(0, len(used_ais[type])):
				parent = used_ais[type][random.choice(rulette)]
				ai_bases[type].append(AI_player(''.join(random.choice(string.ascii_lowercase) for i in range(16)),parent.party, pWeights = parent.give_weights())) 

				ai_bases[type][-1].name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
				dice = random.random()
				if mutation_chance < dice:
					ai_bases[type][-1].mutate(mutation_amplificator)
		if ai_bases["fas_players"][0] == ai_bases["fas_players"][1]:
			print("UZ su rovnake")
		#winsound.Beep(1000, 75)


#winsound.Beep(2500, 500)
if runtype == "discord":
	client.run('')
elif runtype == "ai_train":
#try:
	loop = asyncio.get_event_loop()
	loop.run_until_complete(train())
#except:
	#print('error during training')

	for type in ai_bases:
		for base in ai_bases[type]:
			#base.save_models_to_json()
			i=0

