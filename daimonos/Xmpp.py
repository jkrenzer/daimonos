import sleekxmpp
from sleekxmpp.xmlstream import JID

from Commands import Shell

class ClientBase(sleekxmpp.ClientXMPP):
    """
    Base-Class for XMPP-client operations
    """

    # Generic configuration

    def __init__(self, jid, password, nick="Daimonos"):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Group Chats "MUC"
        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
        
    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

class SingleQuery(ClientBase):
    
    def __init__(self, jid, password, query, nick=None):
        super(ClientBase, self).__init__(jid,password,nick)
        self.query = query
        self.add_event_handler("session_start", self.start)
        
    def start(self, event):
        try:
            shell = Shell(self)
            result = shell.interpret(self.query)
        finally:
            self.disconnect(wait=True)
        except Shell.Exception e:
            return None
        except:
            return None
        return result
        

class Daemon(ClientBase):
        
    def __init__(self, jid, password, nick=None):
        super(ClientBase, self).__init__(jid,password,nick)
        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            try:
                shell = Shell(self)
                result = shell.interpret(self.query)
                self.send_message(mto=msg['from'], mbody=result % jid.full)
            except Shell.Exception e:
                self.send_message(mto=msg['from'], mbody="An error occured while executing.")
            except:
                self.send_message(mto=msg['from'], mbody="A critical error occured.")
