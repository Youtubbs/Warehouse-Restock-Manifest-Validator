class ManifestError(Exception):
    """Base class for every error raised by this package"""


class ManifestNotFoundError(ManifestError):
    """The manifest file does not exist"""


class ManifestFormatError(ManifestError):
    """The manifest exists but is not a JSON list of rows"""
