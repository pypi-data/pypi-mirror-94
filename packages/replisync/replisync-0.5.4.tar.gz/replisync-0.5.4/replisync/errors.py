class ReplisyncError(Exception):
    """Control exceptions: to exit politely"""
    pass


class ConfigError(ReplisyncError):
    """Error in some configuration entry"""
    pass
