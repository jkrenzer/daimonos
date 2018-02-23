 
class Subscriptions:
    subscribers = dict()

    def add(self,jid):
        if str(JID(jid).full) not in self.subscribers:
            self.subscribers.update({str(JID(jid).full): None})

    def remove(self,jid):
        self.subscribers.pop(str(JID(jid).full))

    def __getattr__(self,name):
        return self.subscriber[name]

    def __setattr__(self,name,value):
        self.subscriber[name] = value

    def load(self, filename):
        with open(filename) as fp:
            self.subscribers = json.load(fp)

    def try_load(self,filename):
        try:
            self.load(filename)
        except FileNotFoundError:
            return

    def save(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.subscribers,fp)
