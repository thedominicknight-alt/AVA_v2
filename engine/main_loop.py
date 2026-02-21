"""
AVA Core Loop
Routes user input to either home control or the AI reasoning engine.
"""

from core.input import perceive_input
from core.intent import classify_intent
from core.context import weave_context
from core.branching import simulate_branches
from core.reflection import reflect_on_branches
from core.memory import store_possibilities, recall_memory, search_memory
from core.action import output_action
from core.learning import learn_and_evolve
from home.controller import execute_home_command


def ava_core_loop(input_data: str) -> str:
    """
    Main brain of AVA. Given raw user input, decides what to do and returns a response string.
    """

    # --- Built-in memory commands ---
    if "show memory" in input_data.lower():
        return recall_memory()

    if input_data.lower().startswith("search memory for"):
        keyword = input_data.lower().replace("search memory for", "").strip()
        return search_memory(keyword)

    # --- Step 1: Parse the input ---
    parsed = perceive_input(input_data)
    from core.behaviour import log_interaction
    log_interaction(input_data, 'conversation')

    # --- Fast path for simple questions ---
    from core.intent import is_simple_question
    import datetime
    from core.ollama_bridge import ask_ollama
    if is_simple_question(input_data):
        if "time" in input_data.lower():
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"It is {now}"
        if "date" in input_data.lower() or "day" in input_data.lower():
            now = datetime.datetime.now().strftime("%A, %B %d")
            return f"Today is {now}"
        return ask_ollama(input_data)

    # --- Step 2: Classify intent (home control vs. conversation) ---
    intent = classify_intent(parsed)
    print(f"[Loop] Intent classified as: {intent['type']}")

    # --- Step 3: Home control path ---
    if intent["type"] == "home_control":
        result = execute_home_command(intent)
        store_possibilities(
            chosen_branch={"path_id": "home-0", "simulation": input_data},
            rejected_branches=[],
            gpt_response=result
        )
        return result

    # --- Step 4: Conversational AI path ---
    context_web = weave_context(parsed)
    branches = simulate_branches(context_web)
    best_branch = reflect_on_branches(branches)

    output = output_action(best_branch)
    store_possibilities(best_branch, branches, gpt_response=output)
    learn_and_evolve(output)

    return output
