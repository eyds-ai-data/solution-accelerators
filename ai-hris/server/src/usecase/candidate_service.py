from loguru import logger
from typing import Optional, List
from src.repository.database import CosmosDB
from src.domain.candidate import Candidate, CandidateResponse

class CandidateService:
    def __init__(self, cosmosdb: CosmosDB):
        self.cosmosdb = cosmosdb

    async def get_candidate(self, candidate_id: str) -> Optional[CandidateResponse]:
        """
        Use case: Retrieve a single candidate by ID.
        
        Args:
            candidate_id: The candidate ID to retrieve
            
        Returns:
            CandidateResponse object if found, None otherwise
        """
        try:
            candidate = self.cosmosdb.get_by_id(candidate_id)
            if candidate:
                return CandidateResponse(
                    id=candidate.id,
                    candidate_id=candidate.candidate_id,
                    name=candidate.name,
                    email=candidate.email,
                    phone=candidate.phone,
                    position=candidate.position,
                    status=candidate.status,
                    applied_date=candidate.applied_date,
                    experience=candidate.experience,
                    skills=candidate.skills,
                    rating=candidate.rating,
                    notes=candidate.notes
                )
            return None
        except Exception as e:
            logger.error(f"Error in get_candidate use case: {e}")
            raise

    async def list_candidates(self, limit: int = 100) -> List[CandidateResponse]:
        """
        Use case: Retrieve all candidates.
        
        Args:
            limit: Maximum number of candidates to retrieve
            
        Returns:
            List of CandidateResponse objects
        """
        try:
            candidates = self.cosmosdb.get_all(limit)
            return [
                CandidateResponse(
                    id=c.id,
                    candidate_id=c.candidate_id,
                    name=c.name,
                    email=c.email,
                    phone=c.phone,
                    position=c.position,
                    status=c.status,
                    applied_date=c.applied_date,
                    experience=c.experience,
                    skills=c.skills,
                    rating=c.rating,
                    notes=c.notes
                )
                for c in candidates
            ]
        except Exception as e:
            logger.error(f"Error in list_candidates use case: {e}")
            raise

    async def get_candidates_by_status(self, status: str, limit: int = 100) -> List[CandidateResponse]:
        """
        Use case: Retrieve candidates filtered by status.
        
        Args:
            status: The status to filter by
            limit: Maximum number of candidates to retrieve
            
        Returns:
            List of CandidateResponse objects
        """
        try:
            candidates = self.cosmosdb.get_by_field("status", status, limit)
            return [
                CandidateResponse(
                    id=c.id,
                    candidate_id=c.candidate_id,
                    name=c.name,
                    email=c.email,
                    phone=c.phone,
                    position=c.position,
                    status=c.status,
                    applied_date=c.applied_date,
                    experience=c.experience,
                    skills=c.skills,
                    rating=c.rating,
                    notes=c.notes
                )
                for c in candidates
            ]
        except Exception as e:
            logger.error(f"Error in get_candidates_by_status use case: {e}")
            raise

    async def get_candidates_by_position(self, position: str, limit: int = 100) -> List[CandidateResponse]:
        """
        Use case: Retrieve candidates filtered by position.
        
        Args:
            position: The position to filter by
            limit: Maximum number of candidates to retrieve
            
        Returns:
            List of CandidateResponse objects
        """
        try:
            candidates = self.cosmosdb.get_by_field("position", position, limit)
            return [
                CandidateResponse(
                    id=c.id,
                    candidate_id=c.candidate_id,
                    name=c.name,
                    email=c.email,
                    phone=c.phone,
                    position=c.position,
                    status=c.status,
                    applied_date=c.applied_date,
                    experience=c.experience,
                    skills=c.skills,
                    rating=c.rating,
                    notes=c.notes
                )
                for c in candidates
            ]
        except Exception as e:
            logger.error(f"Error in get_candidates_by_position use case: {e}")
            raise
