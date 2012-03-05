import threading,sys;
#import triagemain as main;
#import moved to bottom

class TriageHandler:
	seenusers = []
	admins = ['Riking','Risugami',']
	iconn = None

#Format: (id, action, message)
#action 1: log it!
	messages = [
(0,0, """Hey. I'll be your automated mod installation helper. To proceed through each prompt, you need to type a number.\n\
To continue, type 0.""")
,(1,0, """Good job! Okay, let's start. Please download and run MCError, at http://bit.ly/t154lG .\n\
If you are having trouble finding the download, say 3. For more info about the tool, say 4.\n\
Once you have downloaded the tool, say 2.""")
,(2,0, """Please run the tool. If you're using Linux, make sure to mark it executable first. Click "Launch Minecraft",\
then close Minecraft once it crashes.\n\
If MCError tells you what's wrong, say 5. If it doesn't, say 6.""")
,(3,0, """Here's a more direct link: https://github.com/medsouz/MinecraftError/downloads Click on the file with the highest version number that does not say testing.""")
,(4,0, """MCError was created by medsouz. The GUI was made by Malqua, and the analysis was made by Riking. To view the code, go to https://github.com/medsouz/MinecraftError""")
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
		print "triage.py ready"

			
	def sayM(self,msg):
		if main.enabled:
			self.iconn.msg(main.mainchannel,msg)
			
	def sayT(self,msg):
		if main.enabled:
			self.iconn.msg(main.triagechannel,msg)
			
	def read(self,msg_id):
		if main.enabled:
			q = messages[msg_id].split('\n')
			for s in q:
				self.iconn.msg(main.triagechannel,q)
			
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
					self.sayM('''Welcome to #risucraft, %s!\
If you want automated mod installing help, say !autohelp and I will assist you.\
If you need help with creating a mod, just ask your question and someone will get to helping you.''' % r[0])


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
	
			
	def onNick(self,oldnick,newnick):
		self.seenusers.append(newnick)
		#for s in self.seenusers:
		#	if(s[0]==oldnick):
		#		s[0]=newnick
	

	def removeUser(self,user):
		self.seenusers.remove(s)
	
	#onMsg moved to bottom
	def handleStartCommand(user,msg):
		self.sayM("%s, please join %s and I will help you." % (user, main.triagechannel))
		self.iconn.invite(user,main.triagechannel)
	
	
	def handleReport(user,msg):
		m = msg[len('report'):]
		self.iconn.send_raw("MS SEND Riking %s" % m)
		self.sayM("INSTALL HELP FOR %s: Error reports - %s" % (user,m))
		
		
	def handleFixHelp(user,msg):
		m = msg[len('fixhelp'):]
		self.sayM("INSTALL HELP FOR %s: Fixing this error - %s" % (user,m))
		
		
	def onMsg(self,user,chan,msg):
		if chan == main.mainchannel:
			if not main.disabled:
				return
			if msg[0] == '!':
				commands = [	('!autohelp',self.handleStartCommand)]
				for c in commands:
					if c[0] in msg:
						c[1].__call__(user,msg)
		if chan == main.triagechannel:
			if msg[0] == '!':
				commands = [	('!report',self.handleReport),
						('!fixhelp',self.handleFixHelp),
						('!shutdown',self.handleShutdown),
						('!disable',self.handleDisable),
						('!enable',self.handleEnable)]
				for c in commands:
					if c[0] in msg:
						c[1].__call__(user,msg)
			a = 0
			try:
				a = int(msg)
				self.read(a)
			except ParseError:
				pass
# (outside class)
import triagemain as main;