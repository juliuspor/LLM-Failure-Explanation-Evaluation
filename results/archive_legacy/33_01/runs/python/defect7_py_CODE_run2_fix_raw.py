@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes: List[Type] = []
    for item in array:
        if item is None:
            raise AttributeError("Parameter array contains None at index; cannot determine class")
        if isinstance(item, type):
            classes.append(item)
            continue
        if isinstance(item, str):
            try:
                resolved = cls.get_class(item)
            except Exception:
                raise AttributeError(f"Cannot find class for name: {item}")
            classes.append(resolved)
            continue
        classes.append(type(item))
    return classes