from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.user import User
from src.domain.ports.user_repository_port import UserRepositoryPort
from src.infrastructure.persistence.models.user_model import UserModel


class PostgresUserRepository(UserRepositoryPort):
    """Adaptador de salida - Repositorio PostgreSQL"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def save(self, user: User) -> User:
        """Guarda un usuario en la DB"""
        db_user = UserModel(
            id=UUID(user.id),
            email=user.email,
            password_hash=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser
            # created_at y updated_at se generan automáticamente
        )
        self._session.add(db_user)
        await self._session.flush()
        await self._session.refresh(db_user)
        return self._to_entity(db_user)
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuario por ID"""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == UUID(user_id))
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Busca usuario por email"""
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.lower())
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def exists_by_email(self, email: str) -> bool:
        """Verifica si existe un usuario con ese email"""
        result = await self._session.execute(
            select(UserModel.id).where(UserModel.email == email.lower())
        )
        return result.scalar_one_or_none() is not None
    
    async def update(self, user: User) -> User:
        """Actualiza un usuario"""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == UUID(user.id))
        )
        db_user = result.scalar_one_or_none()
        
        if db_user:
            self._update_model_from_entity(db_user, user)
            self._session.add(db_user)
            await self._session.flush()
            await self._session.refresh(db_user)
            return self._to_entity(db_user)
        
        return user
    
    async def delete(self, user_id: str) -> bool:
        """Elimina un usuario"""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == UUID(user_id))
        )
        db_user = result.scalar_one_or_none()
        
        if db_user:
            await self._session.delete(db_user)
            await self._session.flush()
            return True
        return False
    
    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """Convierte modelo SQLAlchemy a entidad de dominio"""
        return User(
            id=str(model.id),
            email=str(model.email),
            hashed_password=str(model.password_hash),
            full_name=str(model.full_name),
            is_active=bool(model.is_active),
            is_superuser=bool(model.is_superuser),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    @staticmethod
    def _update_model_from_entity(model: UserModel, entity: User) -> None:
        """Actualiza modelo SQLAlchemy desde entidad de dominio"""
        model.email = entity.email
        model.password_hash = entity.hashed_password
        model.full_name = entity.full_name
        model.is_active = entity.is_active
        model.is_superuser = entity.is_superuser
        # created_at y updated_at se actualizan automáticamente
