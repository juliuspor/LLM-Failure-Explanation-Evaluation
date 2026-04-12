    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is None:
            new_list = []
        else:
            new_list = array.copy()
        new_list.append(element)
        return new_list