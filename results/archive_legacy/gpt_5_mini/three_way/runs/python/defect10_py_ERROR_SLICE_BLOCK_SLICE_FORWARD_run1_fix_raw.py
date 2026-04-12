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
            if len(numeric) == 0:
                raise ValueError(f"{val} is not a valid number.")
            if (numeric.startswith("-") and numeric[1:].isdigit()) or numeric.isdigit():
                try:
                    return int(numeric)
                except ValueError:
                    raise ValueError(f"{val} is not a valid number.")
            raise ValueError(f"{val} is not a valid number.")
        raise ValueError(f"{val} is not a valid number.")
    if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
        return int(val)
    raise ValueError(f"{val} is not a valid number.")