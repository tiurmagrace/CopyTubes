class Vendor:
    def __init__(self, name: str, service: str, contact: str):
        self.name = name
        self.service = service  # Catering, Sound System, etc.
        self.contact = contact
        self.rating = None
        self.contract_signed = False
