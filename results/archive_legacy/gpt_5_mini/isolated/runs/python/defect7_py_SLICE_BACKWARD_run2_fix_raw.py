@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for i, val in enumerate(array):
        if val is None:
            raise AttributeError(f"Parameter at index {i} is None")
        classes.append(type(val))
    return classes
