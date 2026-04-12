@staticmethod
def create_number(val: Optional[str]) -> Optional[Union[int, float]]:
    if val is None:
        return None
    if len(val) == 0:
        raise ValueError('"" is not a valid number.')
    if val.startswith("--"):
        return None

    last_char = val[-1]
    if not last_char.isdigit():
        numeric = val[:-1]

        if last_char in ("l", "L"):
            if not numeric:
                raise ValueError(f"{val} is not a valid number.")
            if (numeric[0] == "-" and len(numeric) > 1 and numeric[1:].isdigit()) or numeric.isdigit():
                return int(numeric)
            raise ValueError(f"{val} is not a valid number.")

        raise ValueError(f"{val} is not a valid number.")

    if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
        return int(val)

    raise ValueError(f"{val} is not a valid number.")