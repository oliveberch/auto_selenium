def to_snake_case(name: str) -> str:
    """Converts a string to a valid Python identifier in snake_case."""
    return "".join(c if c.isalnum() else "_" for c in name).lower() 