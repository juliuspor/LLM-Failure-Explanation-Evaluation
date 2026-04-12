@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

        classes = []
        for item in array:
            # Safely handle any item type; do not call str methods that may not exist
            if item is None:
                classes.append(type(None))
            else:
                classes.append(type(item))
        return classes