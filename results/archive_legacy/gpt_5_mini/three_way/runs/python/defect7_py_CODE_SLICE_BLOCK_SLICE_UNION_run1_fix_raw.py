@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes: List[Type] = []
    for i, item in enumerate(array):
        if item is None:
            raise AttributeError(f"Parameter array[{i}] is None")
        classes.append(type(item))
    return classes