class Company:

    def __init__(self, name: str = "", info: str = "", requirements: str = "", info_collected: bool = False):
        self.name = name
        self.info = info
        self.requirements = requirements
        self.info_collected = info_collected
    
    def to_dict(self):
        return {
            "name": self.name,
            "info": self.info,
            "requirements": self.requirements,
            "info_collected":self.info_collected
        }
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["info"],data["requirements"],data["info_collected"])
                                                                  