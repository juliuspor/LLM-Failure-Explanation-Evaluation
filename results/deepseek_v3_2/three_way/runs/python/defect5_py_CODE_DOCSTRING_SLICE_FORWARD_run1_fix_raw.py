    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is None:
            new_list = []
        else:
            new_list = array.copy()
        new_list.append(element)
        if expected_type is not None:
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to list of expected type {expected_type.__name__}"
                )
        return new_list