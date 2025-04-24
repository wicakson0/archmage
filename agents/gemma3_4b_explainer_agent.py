from smolagents import CodeAgent
from agents import gemma3_4b_model
from tools import db_tools

gemma3_4b_explainer_agent = CodeAgent(
    tools=[db_tools.save_code_summary],
    model=gemma3_4b_model.gemma3_4b,
    add_base_tools=True,
)
