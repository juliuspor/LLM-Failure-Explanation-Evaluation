    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if expected_type is not None and element is not None:
            if not isinstance(element, expected_type):
                raise TypeError(
                    f"Cannot add element of type {type(element).__name__} to list of expected type {expected_type.__name__}"
                )
        new_list = ArrayUtils._copy_list_grow1(array, expected_type)
        new_list[len(new_list) - 1] = element
        return new_list