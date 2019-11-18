def capitaliseFirst(string_in: str) -> str:
    """A utility function that will capitalise only the first character in a string. Unlike str.capitalize() which will lower all other characters in the string."""
    if len(string_in) == 0:
        return ""
    elif len(string_in) == 1:
        return string_in[0].upper()
    elif len(string_in) > 1:
        return string_in[0].upper() + string_in[1:]
