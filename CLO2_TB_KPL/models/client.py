class Client:
    def __init__(self, name: str, contact: str, address: str):
        self.name = name
        self.contact = contact
        self.address = address
        self.event_history = []  # list of event titles
        self.preferences = []    # list of preferences
