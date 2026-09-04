def analyze_quality(function_details):
    issues = []

    for function in function_details:
        if function["lines"] > 30:
            issues.append(
                f"{function['name']} (starts at Line {function['start_line']}): long function"
            )

        if function["arguments"] > 5:
            issues.append(
                f"{function['name']} (starts at Line {function['start_line']}): too many arguments"
            )

        if function["complexity"] > 10:
            issues.append(
                f"{function['name']} (starts at Line {function['start_line']}): "
                f"high complexity ({function['complexity']})"
            )

    return issues


def calculate_health_score(function_details, todos, fixmes):
    score = 100

    for function in function_details:
        if function["lines"] > 30:
            score -= 5
        if function["arguments"] > 5:
            score -= 3
        if function["complexity"] > 10:
            score -= 5

    score -= todos
    score -= fixmes

    return max(0, score)


def get_health_rating(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 50:
        return "Needs Improvement"
    else:
        return "Poor"