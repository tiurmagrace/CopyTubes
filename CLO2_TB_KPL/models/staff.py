class Staff:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role  # MC, Security, Decorator, etc.
        self.schedule = []  # list of event titles
