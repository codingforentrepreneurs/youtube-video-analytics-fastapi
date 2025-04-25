def parse_int_or_fallback(int_str, fallback=0):
    value = fallback
    try:
        value = int(int_str)
    except:
        pass
    return value