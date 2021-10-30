from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label 
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random
class Manager(ScreenManager):
	pass
class Menu(Screen):
	pass
	

class Entity(Image):
	def tick(self):
		pass
	
	def render(self):
		pass

class Game(Screen):
	obstacles = []
	gap = random.randrange(130,150)
	fps = NumericProperty(1/60)
	score=0
	count=0
	def on_pre_enter(self, *args):
		self.ids.player.y=self.height/2
		self.ids.player.speed=0
		for Ob in self.obstacles:
			self.remove_widget(Ob)
			self.obstacles.remove(Ob)
		self.score=0

	def on_enter(self,*args):
		Clock.schedule_interval(self.update, self.fps)
	
	def addObstacle(self, *argas):
		self.gap = random.randrange(130,150)
		obstacle_height=(self.height)*random.randrange(1, 80)/100	
		Ob_short = Obstacle(x=self.width, y=0, height=obstacle_height, width=70)
		Ob_top = Obstacle(x=self.width,y=obstacle_height+self.gap,height=obstacle_height, width=70)
		self.obstacles.append(Ob_short)
		self.add_widget(Ob_short)
		self.add_widget(Ob_top)
		self.obstacles.append(Ob_top)
	
	def animationOb(self, *args):
		for Ob in self.obstacles:
			self.score+=.5
			Ob.x+= Ob.vel
			if Ob.x < -Ob.width:
				self.remove_widget(Ob)
				self.obstacles.remove(Ob)
		
	def on_touch_down(self, *args):
		self.ids.player.speed = self.ids.player.momentum /self.ids.player.mass
	delayAddObstacle=0
	def update(self, *args):
		self.animationOb()
		self.ids.lb.text = 'score: '+str(self.score)
		#Mudar depois na classe Player com erança de Entity
		self.ids.player.speed +=self.ids.player.g
		
		self.ids.player.y +=self.ids.player.speed
		
		#Verifica se o Jogador nao excedeu os limites da tela
		if self.ids.player.y<=0 or self.ids.player.y>= self.height:
				self.gameOver()
		self.delayAddObstacle+=1
		
		#Condiçao para adicionar Obstaculos
		if self.delayAddObstacle >=self.fps*(1/self.fps)*60:
			self.delayAddObstacle = 0
			self.addObstacle()
		
		#Verifica a colisao da parede com o Jogador	
		self.ColisionObstacle_With_Player()
				
		
	def gameOver(self, *args):
		Clock.unschedule(self.update, self.fps)

		self.removeOb()
		App.get_running_app().root.current='gameOver'
		
	def removeOb(self, *agrs):
		for Ob in self.obstacles:
			self.remove_widget(Ob)
			self.obstacles.remove(Ob)

	def ColisionObstacle_With_Player(self, *args):
		for Ob in self.obstacles:
			if Colision().checkColider(Ob, self.ids.player):
				self.gameOver()	

class Conf(Screen):
	def setFps(self):
		Game().fps=float(1/int(self.ids.inputFps.text))
	def stopSound(self):
		global sound
		sound.stop()
		
	def playSound(self):
		global sound
		sound.play()
		sound.loop = True
class Player(Image):
	momentum = NumericProperty(15)
	mass = NumericProperty(1)
	g = NumericProperty(-1)
	speed =NumericProperty(0)

class Colision:
	def checkColider(self, obj1, obj2):
		return self.colider(obj1, obj2)
		
	def colider(self, obj1, obj2):
		if obj1.x + obj1.width > obj2.x and	 obj1.x<obj2.x and obj1.y + obj1.height >obj2.y and obj1.y <obj2.y:
			return True
		return False
class GameOver(Screen):
	pass
class Obstacle(Image):
	vel = NumericProperty(-10)	
class myApp(App):
	def build(self):
		return Manager()
sound = SoundLoader.load('mySound3.mp3')
sound.play()
sound.loop = True
myApp().run()