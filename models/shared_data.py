from peewee import Model, AutoField, TextField, SqliteDatabase, DoesNotExist
from typing import Optional, List, Dict


# Global DB object
_db_instance: Optional[SqliteDatabase] = None


def set_db_path(db_path: str):
    """Initializes the global DB instance."""
    global _db_instance
    if _db_instance is None or _db_instance.database != db_path:
        _db_instance = SqliteDatabase(db_path)
        _db_instance.connect()
        _db_instance.create_tables([SharedData])


class SharedData(Model):
    id = AutoField()
    source_filepath = TextField()
    code = TextField()
    core_abstraction = TextField()
    abstraction_relationship = TextField()
    description = TextField()

    class Meta:
        database = _db_instance  # Placeholder, updated by set_db_path()


def insert_shared_data(
    source_filepath: str,
    code: str,
    core_abstraction: str,
    abstraction_relationship: str,
    description: str,
) -> SharedData:
    return SharedData.create(
        source_filepath=source_filepath,
        code=code,
        core_abstraction=core_abstraction,
        abstraction_relationship=abstraction_relationship,
        description=description,
    )


def read_shared_data_by_id(entry_id: int) -> Optional[SharedData]:
    try:
        return SharedData.get(SharedData.id == entry_id)
    except DoesNotExist:
        return None


def read_all_shared_data() -> List[SharedData]:
    return list(SharedData.select())


def update_shared_data(entry_id: int, updated_fields: Dict[str, str]) -> bool:
    try:
        query = SharedData.update(updated_fields).where(SharedData.id == entry_id)
        rows_modified = query.execute()
        return rows_modified > 0
    except Exception as e:
        print(f"Error updating record: {e}")
        return False


def delete_shared_data(entry_id: int) -> bool:
    try:
        entry = SharedData.get(SharedData.id == entry_id)
        entry.delete_instance()
        return True
    except DoesNotExist:
        return False
