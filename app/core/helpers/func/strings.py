import re


def camel_to_snake(name: str) -> str:
    """
    Convert CamelCase or camelCase string to snake_case.

    Examples:
        camel_to_snake("CamelCaseExample") ➜ "camel_case_example"
        camel_to_snake("userID") ➜ "user_id"

    Args:
        name (str): String in camelCase or CamelCase format.

    Returns:
        str: Converted snake_case string.
    """
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)  # Handle transition from lower → Upper
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)  # Handle lower or number → Upper
    return name.lower()


def snake_to_camel(name: str, upper_first: bool = True) -> str:
    """
    Convert snake_case string to CamelCase or camelCase.

    Examples:
        snake_to_camel("snake_case_example") ➜ "SnakeCaseExample"
        snake_to_camel("snake_case_example", upper_first=False) ➜ "snakeCaseExample"

    Args:
        name (str):
            String in snake_case format.
        upper_first (bool):
            If True -> CamelCase (PascalCase).
            If False -> camelCase.

    Returns:
        str: Converted name in camelCase or CamelCase.
    """
    parts = name.split('_')
    # Capitalize each part
    camel = ''.join(word.capitalize() for word in parts)
    # For lowerCamelCase: make first letter lowercase
    if not upper_first:
        camel = camel[0].lower() + camel[1:]
    return camel
