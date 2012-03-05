from irc import Irc;
#from triage import TriageHandler;
import threading;
import passwordholder;

#config stuff
mainchannel = '#risucraftt'
triagechannel = '#modinstallhelp'
#initial enable state. 0 = disabled, -1 = testing, 1 = enabled
enabled = -1
######
iconn = Irc()
iconn.nick = 'InstallHelper'
iconn.ident = 'RikBots'
iconn.realname = 'Bot'

def init1():
	global ircthread,iconn;
	iconn.on_ready.__iadd__(init2)
	ircthread = threading.Thread(target=iconn.connect,args=("irc.esper.net",6667))
	ircthread.start()


def init2():
	global iconn,triageInst;
	print "identifying to nickserv"
	iconn.msg("NickServ","IDENTIFY %s %s" % (passwordholder.nickservUser,passwordholder.nickservPass))
	print "joining channels"
	iconn.join(triagechannel)
	iconn.join(mainchannel)
	triageInst = TriageHandler(iconn)


def invite(nick):
	iconn.invite(nick,mainchannel)
	

def shutdown():
	disable()
	iconn.quit()


def disable():
	global enabled;
	enabled = 0


def enable():
	global enabled;
	enabled = 1


def testEnable():
	global enabled;
	enabled = -1


if __name__ == "__main__":
	init1()

from triage import TriageHandler;
