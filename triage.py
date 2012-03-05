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

#user statuses
	STARTING = 0
	MAINMENU = 1
	MCERROR = 2
	MODHELP = 3
	OTHERMENU = 4
	ADMINMENU = 5
	INVITED = 6
	#deprecated^

	def __init__(self,ircconnection):
		self.iconn = ircconnection
		self.iconn.on_channel_msg.__iadd__(self.onMsg)
		self.iconn.on_join.__iadd__(self.onJoin)
		self.iconn.on_part.__iadd__(self.onPart)
		self.iconn.on_quit.__iadd__(self.onQuit)
		self.iconn.on_kick.__iadd__(self.onKick)
		print "triage hooks registered"

	
	def sayOLD(self,msg):
		#deprecated^
		if main.enabled:
			self.iconn.msg(main.triagechannel,msg)
			
	def say(self,msg):
		if main.enabled:
			self.iconn.msg(main.mainchannel,msg)
			
	def onJoin(self,chan,user):
		print "%s joined %s" % (user,chan)
		if user == self.iconn.nick:
			return
		elif chan == main.mainchannel:
			if not user in seenusers:
				self.say("Welcome to #risucraft, "+user+"! If you want automated mod installing help, say !autohelp.")
				seenusers.append(user)
			

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
			if msg[0:0] == '!': ##################!!!!!!!!!!!!!!! check this
				keyword = '!autohelp'
				if msg[:len(keyword)] == keyword:
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
