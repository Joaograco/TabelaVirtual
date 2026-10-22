from argon2 import PasswordHasher

class Encryption():
    def __init__(self) -> None:
        self.hasher = PasswordHasher()

    def hash(self, str_to_hash:str) -> str:
        str_hashed = self.hasher.hash(str_to_hash)
        return str_hashed
    
    def verify_from_db(self, str_from_user:str, str_from_db:str) -> bool:
        is_valid = self.hasher.verify(str_from_db, str_from_user)
        return is_valid