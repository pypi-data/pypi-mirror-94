
class bombaatCloudError(Exception):
    """Base exception for cloud."""
    pass

class bombaatSSOError(bombaatCloudError):
    """Exception for SSO."""
    pass

class SAMLParserError(bombaatSSOError):
    """SAML related error"""
    pass

class SSOConnectionError(bombaatSSOError):
    """Raised when the provided SSO Auth failed or could not be validated."""
    pass

class SSOLoginError(bombaatSSOError):
    pass

class SSOFileReadError(bombaatSSOError):
    """Exception raised when there is config file issue."""
    pass

class FileNotFoundError(bombaatSSOError):
    """Exception raised when there is config file issue."""
    pass

class ProfileNotFound(bombaatSSOError):
    """Exception raised when profile not found in config"""
    pass
