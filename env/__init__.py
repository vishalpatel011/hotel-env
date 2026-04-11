__all__ = ["HotelEnv", "HotelEnvOpen"]


def __getattr__(name):
    if name == "HotelEnv":
        from env.environment import HotelEnv

        return HotelEnv
    if name == "HotelEnvOpen":
        from env.openenv_env import HotelEnvOpen

        return HotelEnvOpen
    raise AttributeError(f"module 'env' has no attribute {name!r}")
