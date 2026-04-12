@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        if len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        classes = []
        for idx, item in enumerate(array):
            if item is None:
                raise AttributeError(f"at index {idx}")
            classes.append(type(item))
        return classes
