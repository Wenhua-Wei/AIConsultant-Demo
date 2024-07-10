class User:
    def __init__(self,telephone:str,company_name:str,name:str,position:str) -> None:
        self.telephone=telephone
        self.company_name=company_name
        self.name=name
        self.position=position
    
    def to_dict(self):
        return {
            'telephone': self.telephone,
            'company_name': self.company_name,
            'name': self.name,
            'position': self.position
        }