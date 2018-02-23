import sleekxmpp
from sleekxmpp.xmlstream import JID

class Daemon(sleekxmpp.ClientXMPP):
    subscription_file = "/tmp/subscriptions.json"
    """
    A simple SleekXMPP bot that will echo messages it
    receives, along with a short thank you message.
    """

    def __init__(self, jid, password):
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

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)
        self.subscribers = Subscriptions()
        self.subscribers.try_load(self.subscription_file)

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
        self.nick = "Tages-Dämon"
        self.commands = {
            "addsubscriber": re.compile("add\s*subscriber\s(\S*)"),
            "listsubscribers": re.compile("list\s*subscribers\s"),

        }

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

            if self.commands["addsubscriber"].match(msg['body']):
                cmd = self.commands["addsubscriber"].match(msg['body'])
                jid = JID(cmd.group(1))
                self.subscribers.add(jid.full)
                self.subscribers.save(self.subscription_file)
                self.send_message(mto=msg['from'], mbody="%s wurde als Subscriber hinzugefügt." % jid.full)
            else:
                user_jid = JID(msg['from'])
                user_name = user_jid.user
                self.send_message(mto=msg['from'], msubject='Tagesinformationen', mbody=self._motd(name))

    def _motd(self,name):
        """
        Send our message of the day (again).
        """
        ourtime = datetime.now()
        message = "Hallo %s!\n\n" % name
        message += "Es ist %s.\n" % ourtime.strftime("%A, %d. %B %Y %H:%M")
        message += it_is() + "\n"
        message += "Monatselement: %s\nTagesherrscher: %s" % (month_elements[ourtime.month-1], day_sovereigns[ourtime.weekday()])
        return message

    #def send_motd(jid):
        #TODO
