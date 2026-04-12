    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            new_list = array.copy()
        else:
            new_list = []
        new_list.append(element)
        
        if expected_type is not None:
            for i, item in enumerate(new_list):
                if item is not None and not isinstance(item, expected_type):
                    raise TypeError(
                        f"Element at index {i} is of type {type(item).__name__}, "
                        f"expected {expected_type.__name__}"
                    )
        
        return new_list