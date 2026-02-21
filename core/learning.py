import json
import os

MEMORY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'memory_logs.json')

def learn_and_evolve(_):
    print("[Learning] Learning and evolving...")

    if not os.path.exists(MEMORY_PATH):
        print("[Learning] No memory file found.")
        return

    with open(MEMORY_PATH, 'r') as f:
        data = json.load(f)

    if not data:
        print("[Learning] Memory is empty.")
        return

    high_score_count = {}
    for entry in data:
        chosen = entry['chosen_branch']
        sim = chosen['simulation']
        score = chosen.get('reflection_score', 0)
        if score >= 1.2:  # arbitrary threshold for "high-quality" thought
            high_score_count[sim] = high_score_count.get(sim, 0) + 1

    print("[Learning] Top winning thoughts so far:")
    for sim, count in sorted(high_score_count.items(), key=lambda x: -x[1]):
        print(f"- {sim}: {count} times")

    # Later: use this to adjust simulation weights or preferred strategies
