"""Common exceptions for this factory."""


class NoSpecsForVariable(Exception):
    """Raise when attempting to access specs of an unknown variable in template."""


class MalformedTemplate(Exception):
    """Raise when yaml template does not meet requirements."""


class NoOrEmptyQueryException(Exception):
    """Raise when factory has no query or empty query."""


class MissingOrExtraVariableException(Exception):
    """Raise when factory is given more or less variables than explicitly specified in
    template."""


class FetchTemplateError(Exception):
    """Raise when template cannot be fetched from url."""
