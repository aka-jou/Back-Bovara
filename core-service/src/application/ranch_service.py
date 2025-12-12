# src/application/ranch_service.py
from typing import List
from uuid import UUID, uuid4
from src.domain.entities.ranch import Ranch
from src.domain.exceptions import RanchNotFoundException, UnauthorizedAccessException
from src.infrastructure.repositories.ranch_repository import RanchRepository
from src.schemas.ranch import RanchCreate, RanchUpdate

class RanchService:
    def __init__(self, ranch_repo: RanchRepository):
        self.ranch_repo = ranch_repo

    def create_ranch(self, ranch_data: RanchCreate, owner_id: UUID) -> Ranch:
        ranch = Ranch(
            id=uuid4(),
            owner_id=owner_id,
            name=ranch_data.name,
            location=ranch_data.location,
            size_hectares=ranch_data.size_hectares,
        )
        
        return self.ranch_repo.create(ranch)

    def get_ranch(self, ranch_id: UUID, owner_id: UUID) -> Ranch:
        ranch = self.ranch_repo.get_by_id(ranch_id)
        
        if not ranch:
            raise RanchNotFoundException(f"Ranch {ranch_id} not found")
        
        if ranch.owner_id != owner_id:
            raise UnauthorizedAccessException("You don't have permission to view this ranch")
        
        return ranch

    def get_all_ranches(self, owner_id: UUID) -> List[Ranch]:
        return self.ranch_repo.get_by_owner(owner_id)

    def update_ranch(self, ranch_id: UUID, ranch_data: RanchUpdate, owner_id: UUID) -> Ranch:
        existing_ranch = self.ranch_repo.get_by_id(ranch_id)
        
        if not existing_ranch:
            raise RanchNotFoundException(f"Ranch {ranch_id} not found")
        
        if existing_ranch.owner_id != owner_id:
            raise UnauthorizedAccessException("You don't have permission to update this ranch")
        
        updated_ranch = Ranch(
            id=existing_ranch.id,
            owner_id=existing_ranch.owner_id,
            name=ranch_data.name or existing_ranch.name,
            location=ranch_data.location or existing_ranch.location,
            size_hectares=ranch_data.size_hectares or existing_ranch.size_hectares,
        )
        
        return self.ranch_repo.update(ranch_id, updated_ranch)

    def delete_ranch(self, ranch_id: UUID, owner_id: UUID) -> bool:
        ranch = self.ranch_repo.get_by_id(ranch_id)
        
        if not ranch:
            raise RanchNotFoundException(f"Ranch {ranch_id} not found")
        
        if ranch.owner_id != owner_id:
            raise UnauthorizedAccessException("You don't have permission to delete this ranch")
        
        return self.ranch_repo.delete(ranch_id)
