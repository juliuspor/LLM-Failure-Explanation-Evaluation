@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for i, value in enumerate(array):
        if value is None:
            raise AttributeError(f"Array element at index {i} is None")
        classes.append(type(value))
    return classes
