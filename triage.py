import triagemain as main;
import threading;
import sys;

class TriageHandler:
	userm = [] #array of tuple (user, status)
	admins = []
	dontkick = []
	#methods = [handleS0,handleS1,handleS2,handleS3,handleS4,handleS5,handleS6] #array of handler methods
	iconn = None

#user statuses
	STARTING = 0
	MAINMENU = 1
	MCERROR = 2
	MODHELP = 3
	OTHERMENU = 4
	ADMINMENU = 5
	INVITED = 6


	def __init__(self,ircconnection):
		self.iconn = ircconnection
		self.iconn.on_channel_msg.registerHandler(self.onMsg)
		self.iconn.on_join.registerHandler(self.onJoin)
		self.iconn.on_part.registerHandler(self.onPart)
		self.iconn.on_quit.registerHandler(self.onQuit)
		self.iconn.on_kick.registerHandler(self.onKick)

	
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
			if(main.enabled == 0):
				return
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
				
#user statuses
#	STARTING = 0
#	MAINMENU = 1
#	MCERROR = 2
#	MODHELP = 3
#	OTHERMENU = 4
#	ADMINMENU = 5
#	INVITED = 6
	def restartUser(self,user):
		self.setUMode(user,STARTING)
		self.say("Okay, going back to the main menu.")
		self.handleS0(user,None)
	
	def invite(self, user, reason=""):
		if(reason and main.enabled == 1): #do NOT send to main channel when testing
			self.iconn.msg(main.mainchannel,reason)
		self.iconn.invite(user,main.mainchannel)
		self.setUMode(user,INVITED)

	def handleS0(self,user,msg):
		self.say("Hello, %s! I am the #risucraft triage bot." % user)
		self.say("Please say the number in this list that best describes your situation:")
		self.say("(1) Mod installing help (2) Mod making help (3) I just want to chat (4) Other")
		self.say("Pick one and type the number.")

		self.setUMode(user,MAINMENU)
	

	def handleS1(self,user,msg):
		n=main.parseChoice(user,msg)
		#additional parsing attempts
		if n==10:
			if "instal" in msg:
				n=1
			elif "makin" in msg:
				n=2
			elif "chat" in msg:
				n=3
			elif "other" in msg:
				n=4
		if n==1:
			self.say('''MCError is a program to log Minecraft's output and errors. To download, go here and click "Downloads" on the right: http://bit.ly/t154lG''')
			self.say("If MCError tells you that it can't figure out your problem, say one again to join #risucraft.")
			self.say("If it solved your problem, you're free to leave. In the case that MCError crashes, say two.")
			self.setUMode(user,MCERROR)

		elif n==2:
			self.say("Okay. If you don't see your problem on the following list, say one. If you do, say the number.")
			self.say("(2) Entities not rendering")
			self.setUMode(user,MODHELP)

		elif n==3:
			self.say("Sure thing. I'll add you to the exempt list so you don't have to go through this again.")
			main.inviteExemptAdd(user)
			self.invite(user,"Inviting %s to chat.")

		elif n==4:
			self.say("(1) Just let me in (2) Admin commands (11) Return to main menu")
			self.setUMode(OTHERMENU)

		elif n==10:

			self.say("I'm sorry, I didn't recognize that. Your message has been logged and will be used to improve this bot. Please try again.")
		elif n==11:
			self.restartUser(user)
			return
		else:
			self.say("That wasn't one of the choices!")


	def handleS2(self,user,msg):
		n=main.parseChoice(user,msg)
		if n==1:
			self.say("Well, I'm sorry that MCError couldn't figure it out for you.")
			self.invite(user,"Inviting %s with a MCError report" % user)
		elif n==2:
			self.say("Hm. Inviting you to "+main.mainchannel)
			self.invite(user,"Inviting %s with a possible MCError failure" % user)
		elif n==11:
			self.restartUser(user)


	def handleS3(self,user,msg):
		n=main.parseChoice(user,msg)
		if n==10:
			self.say("I'm sorry, I didn't recognize that.")
		if n==1:
			self.say("Sure thing.")
			self.invite(user,"Inviting %s for mod help." % user)
		elif n==2:
			self.say("<under construction>")
		elif n==11:
			self.restartUser(user)


	def handleS4(self,user,msg):
		n=main.parseChoice(user,msg)
		if n==10:
			if "admin" in msg:
				n=2
		if n==1:
			self.say("Sure thing.")
			self.invite(user)
		elif n==2:
			#adminship check
			if (self.iconn.get_mode_char(main.triagechannel) == '@') or (self.iconn.get_mode_char(main.mainchannel) == '@'  ):

				self.say("Current mode: %s" % ('Disabled' if not main.enabled else ('Testing' if main.enabled==-1 else 'Enabled')))
				self.say("Use ; to start args, e.g. '5 ;Samantha'")
				if(main.enabled == -1):
					self.say("(1) Enable TriageBot (2) Shut down TriageBot (3) Disable TriageBot (4) Add invite exempt (5) Remove invite exempt")

				elif(main.enabled == 0):
					self.say("(1) Enable TriageBot (2) Shut down TriageBot (3) Enter Testing Mode (4) Add invite exempt (5) Remove invite exempt")

				elif(main.enabled == 1):
					self.say("(1) Disable TriageBot (2) Shut down TriageBot (3) Enter Testing Mode (4) Add invite exempt (5) Remove invite exempt")

				self.setUMode(ADMINMENU)
			else: #not an admin
				self.say("You're not a TriageBot admin!")
		elif n==11:
			self.restartUser(user)
			return


	def handleS5(self,user,msg):
		if not ((self.iconn.get_mode_char(main.triagechannel) == '@') or    (self.iconn.get_mode_char(main.mainchannel) == '@')):
			print "Adminship assertion failed!"
			self.say("Something went wrong. You shouldn't be in this menu.")
			self.setUMode(user,STARTING)
			return
		else:
			n=main.parseChoice(user,msg)
			if n==4 or n==5:
				arg = msg[msg.find(';'):]
				if not arg:
					self.say("Huh? That needs an argument.")
				elif n==4:
					main.inviteExemptAdd(user)
				elif n==5:
					main.inviteExemptDel(user)
			elif n==1:
				if not(main.enabled == 1):
					main.enable()
				else:
					main.disable()
			elif n==3:
				if not(main.enabled == -1):
					main.testEnable()
				else:
					main.disable()
			elif n==2:
				main.shutdown()
			elif n==11:
				self.say("Say something to trigger join.")
				self.setUMode(user,STARTING)

	def handleS6(self,user,msg):
		n=main.parseChoice(user,msg)
		if n==11:
			self.restartUser(user)
			return
		self.say("What are you still in here for? Go join #risucraft! If you want to restart, say 'restart'.")




	methods = [handleS0,handleS1,handleS2,handleS3,handleS4,handleS5,handleS6] #array of handler methods. Declared at end of file, after all def's complete

# (outside class)
