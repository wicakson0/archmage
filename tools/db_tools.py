from typing import Dict
from smolagents import tool, CodeAgent
from models.shared_data import (
    set_db_path,
    insert_shared_data,
    read_all_shared_data,
    update_shared_data,
    delete_shared_data,
)

# Tool Definitions


@tool
def save_code_summary(
    db_path: str,
    source_filepath: str,
    code: str,
    core_abstraction: str,
    abstraction_relationship: str,
    description: str,
) -> str:
    """
    Saves a summarized explanation for a given source code file into the shared database.

    Args:
        db_path: The path to the database where the summary will be saved.
        source_filepath: Path to the source code file.
        code: The raw code content.
        core_abstraction: The main function, class, or logic described in the code.
        abstraction_relationship: How this code relates to other parts of the codebase.
        description: A natural language description of what the file does.

    Returns:
        A confirmation message indicating the file was saved to the database.
    """
    set_db_path(db_path)
    insert_shared_data(
        source_filepath=source_filepath,
        code=code,
        core_abstraction=core_abstraction,
        abstraction_relationship=abstraction_relationship,
        description=description,
    )
    return f"Saved summary for {source_filepath} to {db_path}"


@tool
def get_all_code_summaries(db_path: str) -> str:
    """
    Retrieves all saved code summaries from the shared database.

    Args:
        db_path: The path to the database where summaries are stored.

    Returns:
        A string with all summaries, or a message saying no summaries are found.
    """
    set_db_path(db_path)
    summaries = read_all_shared_data()
    if summaries:
        return "\n".join(
            [
                f"{summary.source_filepath}: {summary.description}"
                for summary in summaries
            ]
        )
    return "No summaries found."


@tool
def update_code_summary(
    db_path: str, entry_id: int, updated_fields: Dict[str, str]
) -> str:
    """
    Updates a code summary in the shared database.

    Args:
        db_path: The path to the database where the summary is stored.
        entry_id: The ID of the entry to be updated.
        updated_fields: A dictionary of fields to update with their new values.

    Returns:
        A confirmation message indicating the success or failure of the update.
    """
    set_db_path(db_path)
    success = update_shared_data(entry_id, updated_fields)
    if success:
        return f"Updated code summary for entry ID {entry_id}."
    return f"Failed to update code summary for entry ID {entry_id}."


@tool
def delete_code_summary(db_path: str, entry_id: int) -> str:
    """
    Deletes a code summary from the shared database.

    Args:
        db_path: The path to the database where the summary is stored.
        entry_id: The ID of the entry to be deleted.

    Returns:
        A confirmation message indicating the success or failure of the deletion.
    """
    set_db_path(db_path)
    success = delete_shared_data(entry_id)
    if success:
        return f"Deleted code summary for entry ID {entry_id}."
    return f"Failed to delete code summary for entry ID {entry_id}."
