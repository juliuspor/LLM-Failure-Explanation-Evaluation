@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        if len(array) == 0:
            return []
        classes: List[Optional[Type]] = []
        for item in array:
            if item is None:
                classes.append(None)
            else:
                classes.append(type(item))
        return classes
