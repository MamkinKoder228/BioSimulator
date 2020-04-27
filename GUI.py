from random import randint,uniform
from time import sleep
from tkinter import *
from math import sin,cos,radians,sqrt
import matplotlib.pyplot as plt
import uuid

field_width = 1920
field_height = 1080

Population = 0
Population_history = [0] * 1000
steps = 0
Water = 1
Temp = 10
CO2 = 1
SunEnergy = Water * CO2
Objects = [None] * 4096
Foods = [None] * 200
Speed = 4
MutationChance = 0
ExecMutationChance = 0
Index = 0
FoodIndex = 0

root = Tk()
root.title("Evolution by muxa 0.01a")
root.geometry("1920x1080")
canvas = Canvas(root, bg = "cyan",height = field_height, width = field_width)
canvas.pack()

class Cell:
	def __init__(self, x, y, energy, radius, name, Type, color, DNA, canvas, number):
		global Population,Index
		Population += 1
		self.x = x
		self.y = y
		self.number = number
		self.canvas = canvas
		self.radius = radius
		self.color = color
		self.body = self.canvas.create_oval(x, y, x + radius, y + radius,fill = color)
		self.CheckCollisions()
		self.DNA = DNA
		self.EIP = 0
		self.live = 1
		self.age = 1
		self.Type = Type
		self.energy = energy
		self.MaxAge = 100 * Temp
		self.name = name
		self.infected = 0
		Objects[Index] = self
		self.index = Index
		Index += 1
	
	def die(self):
		if self.live:
			global Population
			self.canvas.delete(self.body)
			self.live = 0
			Objects[self.index] = None
			Population -= 1

	
	def divide(self, energy):
		exec("cell%s = Cell(self.x, self.y + self.radius, energy, self.radius, self.Type + str(self.number + 1),self.Type, self.color, self.DNA, self.canvas, self.number + 1)" % (str(uuid.uuid4().hex)))
	

	def CheckCollisions(self):
		Pos = self.canvas.coords(self.body)
		RandDir = randint(-3, 3)
		if Pos[0] <= 0:
			self.canvas.move(self.body, 3, RandDir)
		
		if Pos[1] >= field_height:
			self.canvas.move(self.body, RandDir, -3)
					
		if Pos[2] >= field_width:
			self.canvas.move(self.body, -3, RandDir)
	
		if Pos[3] <= 0:
			self.canvas.move(self.body, RandDir, 3)
		
	def Sensor(self):
		PosX = self.canvas.coords(self.body)[0] + self.radius / 2
		PosY = self.canvas.coords(self.body)[1] + self.radius / 2
		for target in Objects:
			if target == self or target == None:continue
			TargetX = self.canvas.coords(target.body)[0] + self.radius / 2
			TargetY = self.canvas.coords(target.body)[1] + self.radius / 2
			Distance = sqrt((TargetX - PosX) ** 2 - (TargetY - PosY) ** 2)
			if Distance <= self.radius * 2:
				return True
		return False
			
	def execute(self):
		#self.CheckCollisions()
		
		if self.live == 0 or self.energy <= 0 or self.age > self.MaxAge:
			self.die()
			return 0
			
		if uniform(0.001,1) <= ExecMutationChance:
			MutIndex = randint(0,len(self.DNA) - 4)
			self.DNA[MutIndex] = randint(0,10)
			
		self.age += 1
		if self.EIP >= len(self.DNA):
			self.EIP = 0
		
		######### Jump to addres #######
		if self.DNA[self.EIP] == 0:
			self.energy -= 0.1
			self.EIP = self.DNA[self.EIP + 1]
			
		######## Photo Syntesis ########
		elif self.DNA[self.EIP] == 1:
			self.energy += SunEnergy
			self.EIP += 1
			
		####### NOP #######
		elif self.DNA[self.EIP] == 2:
			self.EIP += 1
			self.energy -= 0.01
			
		###### Die ##########
		elif self.DNA[self.EIP] == 3:
			self.die()
			
		##### Move #####
		elif self.DNA[self.EIP] == 4:
			if self.DNA[self.EIP + 1] == 0:
				self.canvas.move(self.body, 3, 0)
				self.energy -= 0.8
				self.x += 3
			
			if self.DNA[self.EIP + 1] == 1:
				self.canvas.move(self.body, -3, 0)
				self.energy -= 0.8
				self.x += -3
			
			if self.DNA[self.EIP + 1] == 2:
				self.canvas.move(self.body, 0, 3)
				self.energy -= 0.8
				self.y += 3
			
			if self.DNA[self.EIP + 1] == 3:
				self.canvas.move(self.body, 0, -3)
				self.energy -= 0.8
				self.y += -3
			root.update()
			self.EIP += 2
		
		##### Divide ####
		elif self.DNA[self.EIP] == 5:
			if self.energy <= self.DNA[self.EIP + 1]:
				self.energy -= 0.3
			else:
				self.energy -= self.DNA[self.EIP + 1]
				self.divide(self.DNA[self.EIP + 1])
			self.EIP += 2
			
		##### Get cell number #####
		elif self.DNA[self.EIP] == 6:
			if self.number >= self.DNA[self.EIP + 1]:self.EIP = self.DNA[self.EIP + 2]
			else:self.EIP = self.DNA[self.EIP + 3]
			self.energy -= 0.05
		
		#### Get current Energy ####
		elif self.DNA[self.EIP] == 7:
			self.energy -= 0.05
			if self.energy > self.DNA[self.EIP + 1]:self.EIP = self.DNA[self.EIP + 2]
			else:self.EIP = self.DNA[self.EIP + 3]
		
		#### Hibernate (cannot exit, only changing EIP from outside)
		elif self.DNA[self.EIP] == 8:
			pass
		
		#### Set cell number ####
		elif self.DNA[self.EIP] == 9:
			self.number = self.DNA[self.EIP + 1]
			self.EIP += 2
			
		#### Make virus ####
		elif self.DNA[self.EIP] == 10:
			exec('virus%s = Virus(self.x+randint(-90, 90), self.y+randint(-90, 90), self.name, "Virus", self.DNA, self.canvas, "red", 20, self)' % str(uuid.uuid4().hex))
			self.energy -= 1.5
			self.EIP += 1
		
		### Detect ###
		elif self.DNA[self.EIP] == 11:
			if self.Sensor():
				self.EIP = self.DNA[self.EIP + 1]
			else:
				self.EIP = self.DNA[self.EIP + 2]
			self.energy -= 0.1
		
			
		else:
			self.EIP += 1
		
		self.energy -= 0.005
			
class Food:
	def __init__(self, x, y, energy, radius, canvas):
		global FoodIndex
		self.x = x
		self.y = y
		self.radius = radius
		self.energy = energy
		self.canvas = canvas
		self.spdX = -1
		self.spdY = 0
		self.body = canvas.create_oval(x, y, x+radius, y+radius, fill = "gold")
		Foods[FoodIndex] = self
		FoodIndex += 1
		
	def draw(self):
			self.canvas.move(self.body, self.spdX, self.spdY)
			root.update()

class Virus:
	def __init__(self, x, y, name, Type, DNA, canvas, color, radius, parent):
		global Index
		self.name = name
		self.color = color
		self.canvas = canvas
		self.Type = Type
		self.index = Index
		Objects[Index] = self
		Index += 1
		self.DNA = DNA
		self.x = x
		self.y = y
		self.radius = radius
		self.body = self.canvas.create_oval(x, y, x + self.radius, y + self.radius, fill = color)
		self.age = 0
		self.energy = 0
		self.live = 0
		self.infected = 0
		root.update()
	
	def destroy(self):
		self.canvas.delete(self.body)
		Objects[self.index] = None
		
	def search(self):
		PosX = self.canvas.coords(self.body)[0] + self.radius / 2
		PosY = self.canvas.coords(self.body)[1] + self.radius / 2
		
		for target in Objects:
			if target == None or target == self or target.live == 0 or target.infected == 0:continue
			TargetX = self.canvas.coords(target.body)[0] + target.radius / 2
			TargetY = self.canvas.coords(target.body)[1] + target.radius / 2
			
			Distance = sqrt((TargetX - PosX) **2 + (TargetY - PosY) ** 2)
			if Distance <= self.radius * 3:
					target.DNA = self.DNA
					target.infected = 1
					self.destroy()
					break
					 
	
	def execute(self):
		self.search()
		

			
#Note: for cell x, y, energy, radius, name, Type, color, DNA, canvas, number
#For virus: x, y, name, Type, DNA, canvas, color, radius
#DNA = [5, 1]
#DNA for mutations
#DNA = [2]*16
#DNA = [1, 4, 4, 7, 2, 6, 1, 2, 6, 2, 3, 5, 4, 2, 2, 2]
#DNA = [1, 6, 1, 3, 4, 5, 0, 4, 6, 5, 5, 5, 2, 2, 2, 2]
#DNA = [5, 3, 2, 1, 5, 1, 1, 2, 5, 1, 1, 7, 4, 2, 2, 2]
#DNA = [4, 2]
#DNA = [6, 4, 8, 4, 1, 5, 1, 8, 1, 1, 8]
#Sporofitus simpleus
#DNA = [1, 1, 1, 1, 6, 1, 8, 26, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 1, 1, 9, 0, 0, 0, 5, 2, 8]
DNA = [1, 1, 4, 0]
RNA = [1, 1, 10]

def SpawnCells():
	for i in range(50):
		exec('cell%s = Cell(%s, %s, 20, 50, "Cell %s", "Photos longus ", "green", DNA, canvas, 0)' % (str(uuid.uuid4().hex),randint(0,field_width),randint(0,field_height),str(uuid.uuid4().hex)))

SpawnCells()

COVID = Virus(1800, randint(0, 1000), "COVID", "COVID - 20", RNA, canvas, "red", 20)

for i in range(1000):
	for obj in Objects:
		if obj == None:continue
		obj.execute()
		print("-"*20)
		print("")
		print("Имя:%s\nВид:%s\nВозраст:%s\nЭнергия:%s\nДНК:%s\nId:%s" % (obj.name, obj.Type, obj.age, obj.energy, obj.DNA, obj.index))
		root.update()
		Population_history[i] = Population
		sleep(1/Speed)
	
root.mainloop()
#plt.figure()
#plt.plot(Population_history)
#plt.show()
