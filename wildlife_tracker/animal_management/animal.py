from typing import Any, List, Optional, Dict

class Animal:
    def __init__(self, 
                 animal_id: int,
                 species: str,
                 age: Optional[int] = None,
                 health_status: Optional[str] = None) -> None:
        self.animal_id = animal_id
        self.species = species
        self.age = age or 0
        self.health_status = health_status or "Unknown"

    def get_animal_details(animal_id) -> Dict[str, Any]: # was dict[str, Any], I think my python version (3.8) only works with Dict[str, Any] - otherwise it is a syntax error
        pass

    def update_animal_details(animal_id: int, **kwargs: Any) -> None:
        pass
    