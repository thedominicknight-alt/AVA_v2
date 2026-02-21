"""
Action Module
Takes the best branch selected by reflection and generates a response via local Ollama.
"""

from core.ollama_bridge import ask_ollama


def output_action(chosen_branch: dict) -> str:
    """Generate a response for the chosen reasoning branch."""
    print("[Action] Generating response via Ollama.")
    thought = chosen_branch.get("simulation", "")
    response = ask_ollama(thought)
    return response
