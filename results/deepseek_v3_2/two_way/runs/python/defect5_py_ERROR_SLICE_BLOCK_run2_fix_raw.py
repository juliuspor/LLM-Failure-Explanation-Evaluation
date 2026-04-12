    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            new_list = array.copy()
            new_list.append(element)
        else:
            new_list = [element]
        return new_list