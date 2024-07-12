from abc import ABC, abstractmethod
from typing import List

from domain.models.collaboration_affiliation import CollaborationAffiliation


class CollaborationAffiliationRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> List[CollaborationAffiliation]:
        pass
