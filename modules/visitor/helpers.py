def convert_to_camel_case(string):
    return "".join(f"_{c.lower()}" if c.isupper() else c for c in string)
