from dataclasses import dataclass

@dataclass
class PersonCreateDto:
    persontype: str
    firstname: str
    middlename: str
    lastname: str
    emailaddress: str
    phonenumber: str
    phonenumbertypeid: int


