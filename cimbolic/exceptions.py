class DefaultFormulaMissingError(Exception):
    """Raised when a 'NULL' formula is missing for a Variable."""
    pass


class VariableNotFoundError(Exception):
    """Raised when a variable is not found to exist."""
    pass


class VariableNotDefinedError(Exception):
    """Raised when a variable exists but isn't defined properly."""
    pass
