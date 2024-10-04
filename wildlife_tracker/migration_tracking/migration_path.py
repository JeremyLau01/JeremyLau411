from typing import Optional

from wildlife_tracker.habitat_management.habitat import Habitat

class MigrationPath:
    def __init__(self,
                 start_location: Habitat,
                 destination: Habitat,
                 current_date: str,
                 current_location: str,
                 path_id: int)->None:
        self.start_location = start_location
        self.destination = destination
        self.current_date = current_date
        self.current_location = current_location
        self.path_id = path_id

    def get_migration_path_details(path_id) -> dict:
        pass

    def update_migration_path_details(path_id: int, **kwargs) -> None:
        pass