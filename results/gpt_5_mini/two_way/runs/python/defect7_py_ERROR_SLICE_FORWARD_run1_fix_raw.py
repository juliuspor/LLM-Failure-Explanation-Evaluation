@classmethod
def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
    if array is None:
        return None
    elif len(array) == 0:
        return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

    classes = []
    for i, elem in enumerate(array):
        if elem is None:
            # Preserve None entries to reflect unknown/absent values
            classes.append(None)
            continue
        # elem exists; append its type
        try:
            classes.append(type(elem))
        except Exception as e:
            raise TypeError(f"Unable to determine type for element at index {i}: {e}")
    return classes
