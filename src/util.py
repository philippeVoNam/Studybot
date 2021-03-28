import re

def to_snake_case(name):
    name = name.lower()
    return re.sub(
        r'\W', '_', name)
