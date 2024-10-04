from typing import Optional, List

from wildlife_tracker.animal_managment.animal import Animal

class AnimalManager:

    def __init__(self) -> None:
        animals: dict[int, Animal] = {}

    def get_animal_by_id(animal_id: int) -> Optional[Animal]:
        pass

    def register_animal(animal: Animal) -> None:
        pass

    def remove_animal(animal_id: int) -> None:
        pass

    def assign_animals_to_habitat(habitat_id: int, animals: List[Animal]) -> None:
        pass
    