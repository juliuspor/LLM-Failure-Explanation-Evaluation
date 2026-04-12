    @staticmethod
    def add(array, element, expected_type=None):
        if array is not None:
            new_list = array.copy()
        else:
            new_list = []
        new_list.append(element)
        return new_list