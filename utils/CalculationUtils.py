def hex_to_decimal(value) -> int:
    v = value if type(value) is str else str(value)
    return int(v, 16)
