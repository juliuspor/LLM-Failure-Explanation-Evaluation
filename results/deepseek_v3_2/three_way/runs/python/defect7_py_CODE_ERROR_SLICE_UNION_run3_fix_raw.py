    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return []
        
        classes = []
        for element in array:
            classes.append(type(element))
        return classes