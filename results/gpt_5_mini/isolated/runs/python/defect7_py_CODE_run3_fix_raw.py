@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        if len(array) == 0:
            return []
        classes: List[Type] = []
        for elem in array:
            if elem is None:
                classes.append(None)
            elif isinstance(elem, type):
                classes.append(elem)
            elif isinstance(elem, str):
                try:
                    classes.append(cls.get_class(elem))
                except Exception:
                    # Fall back to treating it as a plain string type
                    classes.append(type(elem))
            else:
                classes.append(type(elem))
        return classes