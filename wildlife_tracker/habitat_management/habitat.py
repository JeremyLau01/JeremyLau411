from typing import Any, List, Optional, Dict

#Added
from wildlife_tracker.animal_management.animal import Animal
#Added

class Habitat:

    def __init__(self,
                habitat_id: int,
                geographic_area: str,
                size: int,
                environment_type: str,
                animals: Optional[List[int]] = None) -> None:
        self.habitat_id = habitat_id
        self.geographic_area = geographic_area
        self.size = size
        self.environment_type = environment_type
        # this is Pythonic for
        # if animals is not None:
        #   self.animals = animals
        # else:
        #   self.animals = []
        self.animals = animals or []

    def update_habitat_details(self, **kwargs: Dict[str, Any]) -> None: # was dict[str, Any], I think my python version (3.8) only works with Dict[str, Any] - otherwise it is a syntax error
        pass

    def assign_animals_to_habitat(self, animals: List[Animal]) -> None:
        pass

    def get_animals_in_habitat(self) -> List[Animal]:
        pass

    def get_habitat_details(self) -> dict:
        pass