from typing import Any, Optional

from wildlife_tracker.migration_tracking.migration_path import MigrationPath

class Migration:
    def __init__(self,
                 migration_id: int,
                 migration_path: MigrationPath,
                 start_date: str,
                 species: str,
                 status: str = "Scheduled",
                 duration: Optional[int] = None
                 ):
        self.migration_id = migration_id
        self.migration_path = migration_path
        self.start_date = start_date
        self.species = species
        self.status = status
        self.duration = duration or 0
        

    def get_migration_details(migration_id: int) -> dict[str, Any]:
        pass
    
    def update_migration_details(migration_id: int, **kwargs: Any) -> None:
        pass