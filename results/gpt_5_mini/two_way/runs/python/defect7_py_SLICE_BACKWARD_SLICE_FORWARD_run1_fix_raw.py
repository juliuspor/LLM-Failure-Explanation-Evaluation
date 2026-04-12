@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        classes = []
        for i in range(len(array)):
            try:
                elem = array[i]
                # Only call upper if it's a string to avoid AttributeError
                if isinstance(elem, str):
                    _ = elem.upper()
                classes.append(type(elem))
            except Exception:
                # In case of unexpected errors, append the type if possible, else None
                try:
                    classes.append(type(array[i]))
                except Exception:
                    classes.append(None)
        return classes