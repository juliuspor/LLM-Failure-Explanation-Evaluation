    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        
        classes = []
        for i in range(len(array)):
            elem = array[i]
            if isinstance(elem, str):
                # original code attempted to call upper() on string elements
                _ = elem.upper()
            # For non-string elements, do not call upper(); just record their type (None -> type(None))
            classes.append(type(elem))
        return classes
