@staticmethod
def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
    if array is None:
        if element is None:
            return [None]
        return [element]
    new_list = array.copy()
    new_list.append(element)
    return new_list