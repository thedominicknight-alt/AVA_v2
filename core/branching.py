import random

def simulate_branches(context_web):
    print("[Branching] Simulating branches.")
    branches = []

    for i, context in enumerate(context_web):
        text = context.get('parsed_text', '').lower()

        # Match keywords to topics
        if any(word in text for word in ["quantum", "physics", "uncertainty", "particle"]):
            options = [
                "Quantum uncertainty",
                "Particle-wave duality",
                "Quantum tunneling",
                "Heisenberg principle"
            ]
        elif any(word in text for word in ["time", "relativity", "einstein"]):
            options = [
                "Relativity and time dilation",
                "Spacetime curvature",
                "Twin paradox",
                "Gravity and clocks"
            ]
        elif any(word in text for word in ["focus", "concentration", "productivity"]):
            options = [
                "Deep work strategy",
                "Mindfulness & meditation",
                "Time-blocking & scheduling",
                "Remove distractions & digital detox"
            ]
        elif any(word in text for word in ["philosophy", "meaning", "consciousness", "stoic"]):
            options = [
                "Free will vs determinism",
                "Meaning of existence",
                "The nature of consciousness",
                "Stoicism and internal power"
            ]
        elif any(word in text for word in ["future", "agi", "ai", "machine", "robot"]):
            options = [
                "AI ethics & control",
                "AI evolution & learning",
                "AGI risks & safety",
                "Human-AI collaboration paths"
            ]
        else:
            # Fallback: general thinking
            options = [
                "Provide detailed explanation",
                "Ask clarifying question",
                "Give practical example",
                "Offer deep philosophical view"
            ]

        for j, option in enumerate(options):
            branch = {
                'path_id': f"{i}-{j}",
                'simulation': option,
                'likelihood': round(random.uniform(0.3, 0.9), 2),
                'impact': round(random.uniform(0.3, 0.9), 2),
                'risk_score': round(random.uniform(0.0, 0.3), 2)
            }
            branches.append(branch)

    return branches
