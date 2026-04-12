    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if expected_type is not None and not isinstance(element, expected_type):
            raise TypeError(
                f"Cannot add element of type {type(element).__name__} to array expected to contain {expected_type.__name__} elements"
            )
        if array is None:
            return [element]
        new_list = array.copy()
        new_list.append(element)
        return new_list