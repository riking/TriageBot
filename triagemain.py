from irc import Irc;
from triage import TriageHandler;
import threading;

#config stuff
mainchannel = '#risucraft'
triagechannel = '#risucraftTriage'
nickservUser = 'TriageBot'
nickservPass = 'HzeBdMNDQfyQB7xx'
#initial enable state. 0 = disabled, -1 = testing, 1 = enabled
enabled = -1
######
iconn = Irc()
iconn.nick = 'TriageBot'
iconn.ident = 'RikBots'
iconn.realname = 'triagebot'

def init1():
	global ircthread,iconn;
	iconn.on_ready.registerHandler(init2)
	ircthread = threading.Thread(target=iconn.connect,args=("irc.esper.net",6667))
	ircthread.start()

def init2():
	global iconn,triageInst;
	iconn.msg("NickServ","IDENTIFY %s %s" % (nickservUser,nickservPass))
	iconn.join(triagechannel)
	iconn.join(mainchannel)
	testEnable()
	triageInst = TriageHandler(iconn)
	
def invite(nick):
	iconn.invite(nick,mainchannel)

def inviteExempt(str,flag):
	if(flag):
		#Hostmask
		iconn.send_raw("MODE %s +I %s" % (mainchannel,str))
	else:
		#Account name
		iconn.send_raw("MODE %s +I $a:%s" % (mainchannel,str))
		

def parseChoice(user,s):
#logging wrapper
	a = parseNumber(s)
	parseLog("%s-%i~%s" % (user, a, s))
	return a
	
def parseNumber(s):
	#returns 0 thru 9 or parseRetry()
	try:
		return int(s)
	except TypeError:
		q=['zero','one','two','three','four','five','six','seven','eight','nine']
		for x in range(10):
			if str(x) in s: #numbers embedded in text
				return x
			if q[x] in s: #spelled out the number
				return x
		
		return parseRetry(s)

		
def parseRetry(s):
	#Responses:
	#10: unknown
	#11: "restart"
	q=['restart','retry','start over','back','main menu','do this again','try again']
	for x in q:
		if x in s:
			return 11

	return 10


def parseLog(s):
	pass
	

def shutdown():
	global enabled;
	iconn.msg(triagechannel, "Triage bot shutting down..")
	if not(enabled == -1):
		iconn.msg(mainchannel, "Triage bot shutting down..")
	disable()
	iconn.quit()

def disable():
	global enabled;
	enabled = 0
	iconn.msg(triagechannel, "Disabling TriageBot")
	inviteOff()
	forwardOff()

def enable():
	global enabled;
	iconn.msg(triagechannel, "Enabling TriageBot")
	inviteOn()
	forwardOn()
	enabled = 1
	iconn.msg(mainchannel, "TriageBot is now enabled")

def testEnable():
	global enabled;
	iconn.msg(triagechannel, "Entering test mode")
	inviteOff()
	forwardOff()
	enabled = -1

def inviteOn():
	iconn.send_raw("MODE %s +i" % mainchannel)
	
def inviteOff():
	iconn.send_raw("MODE %s -i" % mainchannel)
	
def forwardOn():
	iconn.send_raw("MODE %s +f #%s" % (mainchannel,triagechannel))
	
def forwardOff():
	iconn.send_raw("MODE %s -f #%s" % (mainchannel,triagechannel))

def inviteExemptAdd(user):
	iconn.send_raw("MODE %s +I %s" % (mainchannel,user))

def inviteExemptDel(user):
	iconn.send_raw("MODE %s -I %s" % (mainchannel,user))
	

if __name__ == "__main__":
	init1()

