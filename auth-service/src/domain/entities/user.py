from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    """Entidad de dominio User - Pura, sin dependencias externas"""
    
    id: str
    email: str
    hashed_password: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @staticmethod
    def create(
        email: str,
        hashed_password: str,
        full_name: str,
        is_superuser: bool = False
    ) -> "User":
        """Factory method para crear un nuevo usuario"""
        return User(
            id=str(uuid.uuid4()),
            email=email.lower().strip(),
            hashed_password=hashed_password,
            full_name=full_name.strip(),
            is_active=True,
            is_superuser=is_superuser,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    def update_password(self, new_hashed_password: str) -> None:
        """Actualiza la contraseña del usuario"""
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Desactiva el usuario"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activa el usuario"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
