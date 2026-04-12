@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    if not hasattr(array, '__len__') or not hasattr(array, '__getitem__'):
        array = list(array)
    if len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
    classes = []
    for elem in array:
        if elem is None:
            raise AttributeError('Element at index is None')
        classes.append(type(elem))
    return classes
