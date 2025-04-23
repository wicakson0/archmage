from tinydb import TinyDB, Query
from typing import Optional


def get_shared_db(db_name: str) -> Optional[TinyDB]:
    try:
        return TinyDB(db_name)
    except Exception as e:
        print(f"Error opening TinyDB database: {e}")
        return None


def init_shared_entry(db_name: str, repo_filepath: str):
    db = get_shared_db(db_name)
    if not db:
        return

    default_data = {
        "repo_filepath": repo_filepath,
        "codebase": [],
        "core_abstractions": [],
        "abstraction_relationships": [],
        "chapters": [],
    }

    if not db.search(Query().repo_filepath == repo_filepath):
        db.insert(default_data)

    db.close()
