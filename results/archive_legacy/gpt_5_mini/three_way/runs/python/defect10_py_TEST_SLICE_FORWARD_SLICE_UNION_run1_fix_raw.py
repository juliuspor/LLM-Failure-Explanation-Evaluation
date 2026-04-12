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
        if last_char in ("l", "L"):
            if len(val) == 1:
                raise ValueError(f"{val} is not a valid number.")
            numeric = val[:-1]
            if numeric == "-":
                raise ValueError(f"{val} is not a valid number.")
            if numeric.isdigit() or (numeric.startswith("-") and numeric[1:].isdigit()):
                return int(numeric)
            raise ValueError(f"{val} is not a valid number.")
        raise ValueError(f"{val} is not a valid number.")
    if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
        return int(val)
    raise ValueError(f"{val} is not a valid number.")