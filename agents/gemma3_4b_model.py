from smolagents import LiteLLMModel

gemma3_4b = LiteLLMModel(
    model_id="ollama/gemma3:4b",
    api_base="http://localhost:11434",
    api_key=None,
    num_ctx=128000,
)
