from abc import ABC, abstractmethod


class PasswordHasherPort(ABC):
    """Puerto de salida - Interfaz para hashear contraseñas"""
    
    @abstractmethod
    def hash(self, password: str) -> str:
        """Hashea una contraseña"""
        pass
    
    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        pass
