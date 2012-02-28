import triagemain as main;
import threading;
import sys;

class TriageHandler:
	userm = [] #array of tuple (user, mode)
	admins = []
	dontkick = []
	methods = [handleS0,handleS1,handleS2,handleS3,handleS4,handleS5,handleS6] #array of handler methods
	iconn = None

	STARTING = 0
	MAINMENU = 1
	MCERROR = 2
	MODHELP = 3
	OTHERMENU = 4
	ADMINMENU = 5
	INVITED = 6


	def __init__(self,object):
		self.iconn = object
		self.iconn.on_channel_msg.registerHandler(self.onMsg)
	
	def say(self,msg):
		self.iconn.msg(main.triagechannel,msg)

	def onJoin(self,chan,user):
		if(chan == main.triagechannel):
			self.setUMode(user,0)
			self.handleS0(user,None)
		if(chan == main.mainchannel):
			if(self.getUMode(user) == 6):
				iconn.kick(user,main.triagechannel,"Thank you for using the Triage Bot")
				self.removeUser(user)
			

	def onPart(self,chan,user):
		if(chan == main.triagechannel):
			self.removeUser(user)
		if(chan == main.mainchannel):
			pass

			
	def onQuit(self,chan,user):
		if(chan == main.triagechannel):
			self.removeUser(user)
		if(chan == main.mainchannel):
			pass

	
	def onMsg(self,user,chan,msg):
		if(chan == main.triagechannel):
			self.methods[self.getUMode(user)] (user,msg)
		elif(chan == main.mainchannel):
			if(msg[:len("TriageBot:")]=="TriageBot:"):
				pass


	def onNick(self,oldnick,newnick):
		for s in self.userm:
			if(s[0]==oldnick):
				s[0]=newnick
	

	def getUMode(self,user):
		for s in self.userm:
			if(s[0]==user):
				return s[1]
		else:
			print "User not found: %s" % user
			self.setUMode(user,0)
			self.say('a weird error has occured with %s. you have been sent to the start' % user)
	

	def setUMode(self,user,val):
		for s in self.userm:
			if(s[0]==user):
				s[1]=val
				break
		else:
			self.userm.append( (user,val) )
		

	def removeUser(self,user):
		for s in self.userm:
			if(s[0]==user): #Works!
				self.userm.remove(s)
				
	#User states
	#0: just joined
	#1: root menu[1234]
	#2: got mcerror[1]
	#3: asked for mod help[12]
	#4: picked Other from main menu[123]
	#5: other>admin commands[1234]
	#6: invited to #risucraft[]
	def restartUser(self,user):
		self.setUMode(user,STARTING)
		self.say("Okay, restarting.")

		self.handleS0(user,None)
	

	def handleS0(self,user,msg):
		self.say("Hello, %s! I am the #risucraft triage bot." % user)
		self.say("Please say the number in this list that best describes your situation:")
		self.say("(1) Mod installing help (2) Mod making help (3) I just want to chat (4) Other")
		self.say("Pick one and type the number.")

		self.setUMode(user,MAINMENU)
	

	def handleS1(self,user,msg):
		n=main.parseNumber(msg)
		
