import threading,sys;
#import triagemain as main;
#import moved to bottom

class TriageHandler:
	userm = [] #array of tuple (user, status)
	#deprecated^
	seenusers = []
	admins = ['Riking']
	dontkick = []
	#deprecated^
	#methods = [handleS0,handleS1,handleS2,handleS3,handleS4,handleS5,handleS6] #array of handler methods
	#deprecated^
	iconn = None

#Format: (id, action, message)
#action 1: log it!
	messages = [
(0,0, """Hey. I'll be your automated mod install helper bot. To proceed through each prompt, you need to type a number.\n\
To continue, type 0.""")
,(1,0, """Good job! Okay, let's start. Please download and run MCError, at http://bit.ly/t154lG .\n\
If you are having trouble finding the download, say 3. For more info about the tool, say 4.\n\
Once you have downloaded the tool, say 2.""")
,(2,0, """Please run the tool. If you're using Linux, make sure to mark it executable first. Click "Launch Minecraft",\
then close Minecraft once it crashes.\n\
If MCError tells you what's wrong, say 5. If it doesn't, say 6.""")
,(3,0, """ """)
,(4,0, """ """)
,(5,0, """Okay. Try to fix the problem, and click "Launch Minecraft" again. Repeat this until it works.\n\
If this solves your problem, please say 8. If you don't know how to fix it, say 7.""")
,(6,1, """Sorry that MCError couldn't automatically detect the issue.\
Please click on both Paste Error and Modloader.txt.\n\
Once it gives the links, say !report <error link> <ml.txt link> and go back to #risucraft.""")
,(7,1, """Please click both Paste Error and ModLoader.txt. Then say !fixhelp <error link> <modloader.txt link> and \
go back to #risucraft.""")
,(8,1, """Thank you for using the mod installation auto-help bot.""")
]



	def __init__(self,ircconnection):
		self.iconn = ircconnection
		self.iconn.on_channel_msg.__iadd__(self.onMsg)
		self.iconn.on_private_notice.__iadd__(self.onNickServReturn)
		self.iconn.on_join.__iadd__(self.onJoin)
		self.iconn.on_part.__iadd__(self.onPart)
		self.iconn.on_quit.__iadd__(self.onQuit)
		self.iconn.on_kick.__iadd__(self.onKick)
		print "triage hooks registered"

	
	def say(self,msg):
		#deprecated^
		if main.enabled:
			self.iconn.msg(main.triagechannel,msg)
			
	def sayM(self,msg):
		if main.enabled:
			self.iconn.msg(main.mainchannel,msg)
			
	def read(self,msg_id):
		if main.enabled:
			
			self.iconn.msg(main.triagechannel
			
	def onJoin(self,chan,user):
		print "%s joined %s" % (user,chan)
		if user == self.iconn.nick:
			return
		elif chan == main.mainchannel:
			if not user in seenusers:
				seenusers.append(user)
				self.iconn.send_raw("ns ACC %s" % user)
				
				
	def onNickServReturn(self,sender,text):
		if sender == "NickServ":
			r = text.split(' ')
			if r[2] == 0: #they do not have a nickserv account
				if not r[0] in seenusers:
					seenusers.append(r[0])
					self.sayM("Welcome to #risucraft, %s! If you want automated mod installing help, say !autohelp and I will assist you." % r[0])


	def onPart(self,chan,user):
		pass
			
	def onQuit(self,user):
		pass

	def onKick(self,chan,user):
		return #will do later
		if user == self.iconn.nick:
			if chan == main.mainchannel:
				self.iconn.msg(main.triagechannel, "Kicked from #risucraft")
				self.iconn.join(main.mainchannel)
				main.shutdown()
	
	def onMsg(self,user,chan,msg):
		if chan == main.mainchannel:
			if msg[0] == '!':
				keyword = '!autohelp'
				if keyword in msg:
					self.handleStartCommand(user)

	def onNick(self,oldnick,newnick):
		self.seenusers.append(newnick)
		#for s in self.seenusers:
		#	if(s[0]==oldnick):
		#		s[0]=newnick
	

	def getUMode(self,user):
		for s in self.userm:
			if(s[0]==user):
				return s[1]
		else:
			print "User not found in user status list: %s" % user
			self.setUMode(user,0)
	

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


# (outside class)
import triagemain as main;
