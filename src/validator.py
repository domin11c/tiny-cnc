def isPort(value: str) -> int | None:
    return value if value.isdigit() and (value := int(value)) and value >= 0 and value <= 65535 else None

def isValidDuration(value: str) -> int | None:
    return value if value.isdigit() and (value := int(value)) and value >= 10 and value <= 300 else None