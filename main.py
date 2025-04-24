import argparse
import os
from models import shared_data
from utils import dir_reader
from agents import gemma3_4b_explainer_agent
from tools import db_tools


def main(repo_filepath: str, db_filepath: str):
    print("🚀 Running archmage...")
    print(f"📁 Repository: {repo_filepath}")
    print(f"📄 DB: {db_filepath}")

    filepaths = dir_reader.list_file_recursive(repo_filepath)
    for filepath in filepaths:
        print(f"✨ Analyzing: {filepath}")
        code = dir_reader.dump_plaintext_file(filepath)

        # Prepare the prompt with correct formatting
        prompt = f"""
        You are Archmage, a specialized agent for deeply understanding source code in software projects.

        filepath: {filepath}
        code: {code}

        Given the code and source_filepath, your task is to:
        1. **Identify Core Abstractions**: Extract the most important classes, functions, or logic blocks from the code.
        2. **Determine Relationships**: Describe how these abstractions interact with each other or with other parts of the codebase (e.g., imports, function calls, shared state, etc).
        3. **Generate a Markdown Description**: Write a structured explanation in markdown format describing:
        - What this file does
        - What the main abstractions are
        - How it relates to the rest of the project
        - Include relevant code snippets if needed
        - Generate a MermaidJS flowchart or dependency graph if useful

        Then, call the `save_code_summary` tool with the following parameters:
        - db_path: {db_filepath}
        - `source_filepath`: path to the file you’re analyzing
        - `code`: the full source code from the file
        - `core_abstraction`: the most important abstraction (e.g. main class or function)
        - `abstraction_relationship`: how the file's abstractions relate to the broader codebase
        - `description`: your markdown explanation (with code and mermaid graph if helpful)

        Be precise, helpful, and insightful — this information will be stored in a database and used for documentation and understanding of large codebases.
        """

        # Run the agent with the formatted prompt
        gemma3_4b_explainer_agent.gemma3_4b_explainer_agent.run(prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run archmage on a given repository and save to a database."
    )
    parser.add_argument(
        "repo_filepath", type=str, help="Path to the source code repository"
    )
    parser.add_argument(
        "db_filepath", type=str, help="Path to the SQLite database file"
    )

    args = parser.parse_args()
    main(args.repo_filepath, args.db_filepath)
