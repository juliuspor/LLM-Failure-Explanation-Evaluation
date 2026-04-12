    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is None:
            array = []
        new_list = array.copy()
        new_list.append(element)
        if expected_type is not None:
            if element is not None and not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to list expecting {expected_type.__name__}"
                )
        return new_list