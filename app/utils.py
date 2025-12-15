import uuid

def is_valid_uuid4(uuid_string: str) -> bool:
    """
    Validates if the given string is a valid UUIDv4 (RFC 4122).
    Checks:
    - It is a valid UUID.
    - Version is 4 (Random).
    - Variant is RFC 4122.
    """
    try:
        val = uuid.UUID(uuid_string, version=4)
        # Check strict version and variant (though validation above version=4 usually covers version)
        if val.version != 4:
            return False
            
        # uuid.RFC_4122 is the constant for 'specified in RFC 4122'
        if val.variant != uuid.RFC_4122:
            return False
            
        # Optional: Enforce canonical format if desired (e.g., lowercase, with dashes)
        # return str(val) == uuid_string.lower()
        
        return True
    except ValueError:
        return False
