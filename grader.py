def grade_action(action, email, step_count):
    score = 0.0

    if action.category == email["category"]:
        score += 0.4
    if action.priority == email["priority"]:
        score += 0.3
    if action.action == email["action"]:
        score += 0.3

    # penalty
    if action.action == "delete" and email["priority"] == "high":
        score -= 0.5
    score -= 0.01 * step_count

    score = max(0.0, min(0.99, score))
    return score, "graded"
