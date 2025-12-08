from decimal import Decimal, ROUND_HALF_UP
from typing import Annotated, get_args, get_origin


def quantize_decimal(value: Decimal | float | str, target_type: type) -> Decimal:
    """
    Quantize a decimal value to match constraints from Annotated[Decimal, ...] (Pydantic v2 condecimal).
    """
    value = Decimal(str(value))

    if get_origin(target_type) is Annotated:
        args = get_args(target_type)

        # Find first constraint object that has `decimal_places`
        constraint = next((a for a in args if hasattr(a, "decimal_places")), None)
        if not constraint or not hasattr(constraint, "decimal_places"):
            raise ValueError("Target type does not define decimal_places.")

        decimal_places = constraint.decimal_places
        return value.quantize(Decimal(f"1.{'0' * decimal_places}"), rounding=ROUND_HALF_UP)

    raise TypeError("Provided type must be Annotated[Decimal, SomeConstraint]")
