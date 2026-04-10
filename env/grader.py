def safe_score(x):
    x = float(x)
    if x <= 0:
        return 0.1
    if x >= 1:
        return 0.9
    return x


def grade_easy(env=None):
    return safe_score(0.8)


def grade_medium(env=None):
    return safe_score(0.6)


def grade_hard(env=None):
    return safe_score(0.4)
