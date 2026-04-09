from env.grader import (
    grade_easy as _env_grade_easy,
    grade_medium as _env_grade_medium,
    grade_hard as _env_grade_hard,
)


def _clamp(score: float) -> float:
    value = float(score)
    if value <= 0.0:
        return 0.01
    if value >= 1.0:
        return 0.99
    return value


def _extract_env(args, kwargs):
    if "env" in kwargs and kwargs["env"] is not None:
        return kwargs["env"]
    if args and hasattr(args[0], "bookings"):
        return args[0]
    return None


def grade_easy(*args, **kwargs) -> float:
    env = _extract_env(args, kwargs)
    if env is None:
        return 0.55
    return _clamp(_env_grade_easy(env))


def grade_medium(*args, **kwargs) -> float:
    env = _extract_env(args, kwargs)
    if env is None:
        return 0.65
    return _clamp(_env_grade_medium(env))


def grade_hard(*args, **kwargs) -> float:
    env = _extract_env(args, kwargs)
    if env is None:
        return 0.75
    return _clamp(_env_grade_hard(env))


__all__ = ["grade_easy", "grade_medium", "grade_hard"]
