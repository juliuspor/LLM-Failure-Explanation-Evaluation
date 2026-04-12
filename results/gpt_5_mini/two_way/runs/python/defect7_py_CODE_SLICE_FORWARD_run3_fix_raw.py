@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return []

        classes = []
        for i in range(len(array)):
            element = array[i]
            if element is None:
                classes.append(None)
            else:
                classes.append(element.__class__)
        return classes