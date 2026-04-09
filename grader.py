def grade_action(action, email, step_count):
    """
    Returns (score, reason)
    Score MUST be strictly between (0,1)
    """

    score = 0.0

    # Expected label
    expected = email["label"].lower()
    action = action.lower()

    # 🎯 Basic correctness
    if expected in action:
        score += 0.6

    # 🎯 Good keywords
    if "reply" in action or "respond" in action:
        score += 0.2

    # 🎯 Efficiency bonus
    if step_count <= 3:
        score += 0.1

    # 🎯 Small random noise (IMPORTANT for avoiding exact 0 or 1)
    import random
    score += random.uniform(0.01, 0.03)

    # ❗ CRITICAL: FORCE STRICT RANGE
    if score <= 0.0:
        score = 0.05
    elif score >= 1.0:
        score = 0.95

    return float(score), "graded"
