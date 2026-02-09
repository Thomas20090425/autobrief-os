class AutoBriefError(Exception):
    """Base app exception."""


class CollectorError(AutoBriefError):
    """Collector failure."""


class ConfigError(AutoBriefError):
    """Config failure."""
