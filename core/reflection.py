def reflect_on_branches(branches):
    print("[Reflection] Reflecting on branches.")

    best_branch = None
    best_score = -1  # start low so any score will beat this

    for branch in branches:
        likelihood = branch.get('likelihood', 0)
        impact = branch.get('impact', 0)
        risk = branch.get('risk_score', 0)

        # Reflection score formula
        score = (likelihood + impact) - risk
        branch['reflection_score'] = round(score, 2)

        print(f"Branch {branch['path_id']} - Score: {score:.2f} ({branch['simulation']})")

        if score > best_score:
            best_score = score
            best_branch = branch

    print(f"[Reflection] Best branch selected: {best_branch['path_id']} with score {best_score:.2f}")
    return best_branch
