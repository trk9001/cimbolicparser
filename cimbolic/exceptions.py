class DefaultFormulaMissingError(Exception):
    """Raised when a 'NULL' formula is missing for a Variable."""
    pass


class VariableNotFoundError(Exception):
    """Raised when a variable is not found to exist."""
    pass


class VariableNotDefinedError(Exception):
    """Raised when a variable exists but isn't defined in a proper manner."""
    pass


class VariableRelatedDataError(Exception):
    """Raised during processing of a variable's related data."""
    pass
