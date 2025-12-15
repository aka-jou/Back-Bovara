from passlib.context import CryptContext
from src.domain.ports.password_hasher_port import PasswordHasherPort


class BcryptPasswordHasher(PasswordHasherPort):
    """Adaptador de salida - Hasher de contraseñas con bcrypt"""
    
    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash(self, password: str) -> str:
        """Hashea una contraseña con bcrypt"""
        return self._context.hash(password)
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide"""
        return self._context.verify(plain_password, hashed_password)
    
    
