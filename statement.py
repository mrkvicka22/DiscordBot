class Statement:
	def __init__(self, ptype, which_text = -1, additional_text = -1): 
		self.text = []
		self.pos_subs = []
		self.sub = []
		self.text2 = "nothing"
		self.type = ptype
		self.input = []
		self.num_of_text = which_text
		if self.type == "start":
			self.extendable = True
			self.text = ["I think, that "]
			self.pos_subs = [["suggestion"]]
			if additional_text != -1:
				self.text.append(", because ")
				self.text2 = self.text[additional_text]
				self.pos_subs = [["suggestion",],["statement"]]


		elif self.type == "suggestion":
			self.extendable = False
			self.text= [" should be ", " should not be "]
			self.pos_subs = [["player"],["role", "party", "hitler", "vote", "action"]]


		elif self.type == "statement":
			self.extendable = True
			self.pos_subs = [["player"],["role", "party", "hitler","action"]]
			self.text = [" is ", " is not "]
			if additional_text != -1:
				self.text.append(" and ", " or ", " xor ")
				self.text2 = self.text[additional_text]
				self.pos_subs = [["player"],["role", "party", "hitler", "action"],["statement"]]


		elif self.type == "player":
			self.extendable = False
			self.pos_subs = []
			self.text = ["danko", "MvKal", "havos", "Roman", "Viktor", "Gabris", "Tomas"]
		elif self.type == "role":
			self.extendable = False
			self.pos_subs = []
			self.text = ["president", "chancellor"]
		elif self.type == "party":
			self.extendable = False
			self.pos_subs = []
			self.text = ["liberal", "fascist", "socialist", "RUSS", "Madar"]
		elif self.type == "hitler":
			self.extendable = False
			self.pos_subs = []
			self.text = ["Hitler"]
		elif self.type == "vote":
			self.extendable = False
			self.pos_subs = []
			self.text = ["voting ja", "voting nein"]
		elif self.type == "action":
			self.extendable = False
			self.pos_subs = [["player"]]
			self.text = ["investigating ", "shooting ", "specially electing ", "gunpointing " ]



		else:
			print("ERR can't assign type to this statement")
		#self.sub = self.pos_subs
		for num, thing in enumerate(self.pos_subs):
			#for num2, thing2 in enumerate(thing):
			self.sub.append(Statement(self.pos_subs[num][0]))


	def assign_sub(self, psub, number):
		if psub.type in self.pos_subs[number]:
			self.sub[number] = psub
		else:
			print("Invalid assignation of sub. Tried to subassign '" + psub.type + "' under '" + self.pos_subs[number].type + "'.")
			return False

	def possible_texts(self):
		return self.text
	def give_code(self):
		foreturn = []
		if len(self.input) > 0:
			for index, subb in enumerate(self.input):
				if self.input[index] > -1:
					#foreturn= foreturn + str(subb)
					foreturn.append(subb)
				#foreturn = foreturn +self.sub[index].give_code()
				try:
					foreturn.extend(self.sub[index].give_code())
				except IndexError:
					i = 0
		return foreturn

	def export(self):

		foreturn = ""
		if self.num_of_text == -1:
			return "/" + self.type + "/"
		if len(self.pos_subs) == 1 and len(self.sub) >= 1:
			foreturn = self.text[self.num_of_text]+self.sub[0].export()
		if len(self.pos_subs) == 2 and len(self.sub) >= 2:
			foreturn = self.sub[0].export() + self.text[self.num_of_text] + self.sub[1].export()
		if self.type == "start" and self.text2 != "nothing":
			foreturn = self.text[self.num_of_text] + self.sub[0].export() + self.text2 + self.sub[1].export()
		if len(self.pos_subs) == 0:
			return self.text[self.num_of_text]
		return foreturn

