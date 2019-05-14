import copy
import pyperclip

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
				self.text.append(" because ")
				self.text2 = self.text[additional_text]
				self.pos_subs = [["suggestion",],["statement"]]


		elif self.type == "suggestion":
			self.extendable = False
			self.text= [" should be "]
			self.pos_subs = [["player"],["role", "party", "hitler", "action"]]


		elif self.type == "statement":
			self.extendable = True
			self.pos_subs = [["player"],["role", "party", "hitler", "action"]]
			self.text = [" is ", " is not "]
			if additional_text != -1:
				self.text.append(" and ", " or ", " xor ")
				self.text2 = self.text[additional_text]
				self.pos_subs = [["player"],["role", "party", "hitler", "action"],["statement"]]


		elif self.type == "player":
			self.extendable = False
			self.pos_subs = []
			self.text = ["danko", "mvkal", "havos"]
		elif self.type == "role":
			self.extendable = False
			self.pos_subs = []
			self.text = ["president", "chancellor"]
		elif self.type == "party":
			self.extendable = False
			self.pos_subs = []
			self.text = ["liberal", "fascist", "socialist"]
		elif self.type == "hitler":
			self.extendable = False
			self.pos_subs = []
			self.text = ["Hitler", "not Hitler"]
		elif self.type == "action":
			self.extendable = False
			self.pos_subs = [["player"]]
			self.text = ["investigating ", "shooting ", "specially electing ", "gunpointing" ]


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

				temp = Statement(current_sub)

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
				temp = Statement(txt)
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

def main():
	done = False
	global base  
	base = Statement("start", 0, 1)
	optcode = []
	print("Enter optional code, otherwise just enter")
	optcode = list(map(int, input().split()))
	create_statement_for(base, optcode)
	print("Final text reads: " + print_state())
	print("Code is:")
	supercode = base.give_code()
	print(*supercode)
	print(supercode)
	
	supercode = ' '.join([str(i) for i in supercode])
	pyperclip.copy(supercode)



main()




