@classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()

        classes = []
        for item in array:
            try:
                if isinstance(item, str):
                    _ = item.upper()
            except Exception:
                # ignore any issues with upper(); we still want the item's type
                pass
            classes.append(type(item))
        return classes