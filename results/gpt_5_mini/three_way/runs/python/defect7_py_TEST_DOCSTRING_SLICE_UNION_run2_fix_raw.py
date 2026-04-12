@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        # Return a new empty list for empty input to avoid sharing mutable default
        if len(array) == 0:
            return []
        classes: List[Type] = []
        for item in array:
            if item is None:
                classes.append(type(None))
            else:
                classes.append(type(item))
        return classes