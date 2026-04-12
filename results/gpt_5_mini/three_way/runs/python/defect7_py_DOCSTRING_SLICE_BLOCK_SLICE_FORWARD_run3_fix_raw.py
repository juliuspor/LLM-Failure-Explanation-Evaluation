@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes: List[Optional[Type]] = []
    for item in array:
        if item is None:
            classes.append(None)
            continue
        # If a string was provided, try to resolve it to a class name
        if isinstance(item, str):
            try:
                resolved = cls.get_class(item)
            except Exception:
                # Fall back to the str type if resolution fails
                resolved = str
            classes.append(resolved)
        else:
            classes.append(type(item))
    return classes