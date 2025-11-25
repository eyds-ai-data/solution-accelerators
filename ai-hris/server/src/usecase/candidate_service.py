from loguru import logger
from typing import Optional, List
from src.repository.database import CosmosDB, CosmosDBRepository
from src.domain.candidate import Candidate, CandidateResponse

class CandidateService:
    def __init__(self, cosmosdb: CosmosDB):
        self.cosmosdb = cosmosdb
        # Use 'candidates' container, or create with default if not specified
        self.candidate_repo = CosmosDBRepository(cosmosdb, Candidate, container_name="candidates")

    async def get_candidate(self, candidate_id: str) -> Optional[CandidateResponse]:
        """
        Use case: Retrieve a single candidate by ID.
        
        Args:
            candidate_id: The candidate ID to retrieve
            
        Returns:
            CandidateResponse object if found, None otherwise
        """
        try:
            candidate = self.candidate_repo.get_by_id(candidate_id, id_field="candidateId")
            if candidate:
                return CandidateResponse(**candidate.model_dump())
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
            candidates = self.candidate_repo.get_all(limit)
            return [CandidateResponse(**c.model_dump()) for c in candidates]
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
            candidates = self.candidate_repo.get_by_field("status", status, limit)
            return [CandidateResponse(**c.model_dump()) for c in candidates]
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
            candidates = self.candidate_repo.get_by_field("position", position, limit)
            return [CandidateResponse(**c.model_dump()) for c in candidates]
        except Exception as e:
            logger.error(f"Error in get_candidates_by_position use case: {e}")
            raise
