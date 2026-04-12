# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.

from typing import List, Optional, Any, TypeVar, Type

T = TypeVar('T')


class ArrayUtils:
    """
    Operations on arrays (lists in Python).
    
    This class tries to handle None input gracefully.
    An exception will not be thrown for a None list input.
    """
    
    # Empty immutable lists
    EMPTY_OBJECT_LIST: List[Any] = []
    EMPTY_STRING_LIST: List[str] = []
    EMPTY_INT_LIST: List[int] = []
    EMPTY_FLOAT_LIST: List[float] = []
    EMPTY_BOOL_LIST: List[bool] = []
    
    # The index value when an element is not found
    INDEX_NOT_FOUND: int = -1
    
    def __init__(self):
        """ArrayUtils instances should NOT be constructed in standard programming."""
        pass
    
    # ----------------------------------------------------------------------
    # Basic methods
    # ----------------------------------------------------------------------

    @staticmethod
    def to_string(array: Optional[List[Any]], string_if_null: str = "{}") -> str:
        """
        Outputs an array as a String, treating None as an empty array.
        
        Args:
            array: The list to get a string for, may be None
            string_if_null: The string to return if the array is None
            
        Returns:
            String representation of the array
        """
        if array is None:
            return string_if_null
        return str(array).replace('[', '{').replace(']', '}')

    @staticmethod
    def is_equals(array1: Optional[List[Any]], array2: Optional[List[Any]]) -> bool:
        """
        Compares two arrays, using equals().
        
        Args:
            array1: The left hand array to compare, may be None
            array2: The right hand array to compare, may be None
            
        Returns:
            True if the arrays are equal
        """
        return array1 == array2

    @staticmethod
    def to_map(array: Optional[List[Any]]) -> Optional[dict]:
        """
        Converts the given array into a dict. 
        Each element must be an array/list of at least two elements.
        
        Args:
            array: The array to convert, may be None
            
        Returns:
            A dict created from the array, or None if input is None
            
        Raises:
            ValueError: If an element is not valid (length < 2)
        """
        if array is None:
            return None
        
        result = {}
        for i, item in enumerate(array):
            if isinstance(item, (list, tuple)):
                if len(item) < 2:
                    raise ValueError(f"Array element {i}, '{item}', has a length less than 2")
                result[item[0]] = item[1]
            elif isinstance(item, dict):
                 # Handle map entries/dicts if passed
                 result.update(item)
            else:
                 raise ValueError(f"Array element {i}, '{item}', is neither of type Map.Entry nor an Array")
        return result

    @staticmethod
    def to_array(*items: T) -> List[T]:
        """
        Create a type-safe generic array.
        
        Args:
            *items: variable arguments
            
        Returns:
            The items as a list
        """
        return list(items)

    @staticmethod
    def to_primitive(array: Optional[List[Any]], value_for_null: Any = None) -> Optional[List[Any]]:
        """
        Converts an array of objects to primitives. 
        In Python, this is technically a no-op/copy as lists handle all types,
        but it can handle None values by replacing them with a default.
        
        Args:
            array: The list to convert, may be None
            value_for_null: The value to insert if None found (e.g. 0 for int/boolean equivalence)
            
        Returns:
            A list of primitives, None if null input
        """
        if array is None:
            return None
        if len(array) == 0:
            return []
            
        result = []
        for item in array:
            if item is None and value_for_null is not None:
                result.append(value_for_null)
            else:
                result.append(item)
        return result

    @staticmethod
    def to_object(array: Optional[List[Any]]) -> Optional[List[Any]]:
        """
        Converts an array of primitives to objects.
        In Python, this is a no-op/copy.
        
        Args:
            array: The list to convert, may be None
            
        Returns:
            A list of objects, None if null input
        """
        if array is None:
            return None
        return array.copy()

    # ----------------------------------------------------------------------
    # Clone methods
    # ----------------------------------------------------------------------
    
    @staticmethod
    def clone(array: Optional[List[T]]) -> Optional[List[T]]:
        """
        Shallow clones a list returning a copy and handling None.
        
        Args:
            array: The list to shallow clone, may be None
            
        Returns:
            The cloned list, None if None input
        """
        if array is None:
            return None
        return array.copy()
    
    # ----------------------------------------------------------------------
    # isEmpty methods
    # ----------------------------------------------------------------------
    
    @staticmethod
    def is_empty(array: Optional[List[Any]]) -> bool:
        """
        Checks if a list is empty or None.
        
        Args:
            array: The list to test
            
        Returns:
            True if the list is empty or None
        """
        if array is None or len(array) == 0:
            return True
        return False
    
    # ----------------------------------------------------------------------
    # indexOf methods
    # ----------------------------------------------------------------------
    
    @staticmethod
    def index_of(array: Optional[List[T]], object_to_find: T, start_index: int = 0) -> int:
        """
        Finds the index of the given object in the list.
        
        Args:
            array: The list to search through, may be None
            object_to_find: The object to find, may be None
            start_index: The index to start searching at
            
        Returns:
            The index of the object within the list, -1 if not found or None list
        """
        if array is None:
            return ArrayUtils.INDEX_NOT_FOUND
        if start_index < 0:
            start_index = 0
        if object_to_find is None:
            for i in range(start_index, len(array)):
                if array[i] is None:
                    return i
        else:
            for i in range(start_index, len(array)):
                if object_to_find == array[i]:
                    return i
        return ArrayUtils.INDEX_NOT_FOUND
    
    @staticmethod
    def last_index_of(array: Optional[List[T]], object_to_find: T, start_index: int = None) -> int:
        """
        Finds the last index of the given object within the list.
        
        Args:
            array: The list to traverse backwards looking for the object, may be None
            object_to_find: The object to find, may be None
            start_index: The start index to traverse backwards from. If None, starts from end.
            
        Returns:
            The last index of the object within the list, -1 if not found or None list
        """
        if array is None:
            return ArrayUtils.INDEX_NOT_FOUND
            
        if start_index is None or start_index >= len(array):
            start_index = len(array) - 1
        elif start_index < 0:
            return ArrayUtils.INDEX_NOT_FOUND
            
        if object_to_find is None:
            for i in range(start_index, -1, -1):
                if array[i] is None:
                    return i
        else:
            for i in range(start_index, -1, -1):
                if object_to_find == array[i]:
                    return i
        return ArrayUtils.INDEX_NOT_FOUND

    @staticmethod
    def contains(array: Optional[List[T]], object_to_find: T) -> bool:
        """
        Checks if the object is in the given list.
        
        Args:
            array: The list to search through
            object_to_find: The object to find
            
        Returns:
            True if the list contains the object
        """
        return ArrayUtils.index_of(array, object_to_find) != ArrayUtils.INDEX_NOT_FOUND
    
    # ----------------------------------------------------------------------
    # addAll methods
    # ----------------------------------------------------------------------
    
    @staticmethod
    def add_all(array1: Optional[List[T]], array2: Optional[List[T]]) -> Optional[List[T]]:
        """
        Adds all the elements of the given lists into a new list.
        
        Args:
            array1: The first list whose elements are added to the new list
            array2: The second list whose elements are added to the new list
            
        Returns:
            The new list, None if both lists are None
        """
        if array1 is None:
            return ArrayUtils.clone(array2)
        elif array2 is None:
            return ArrayUtils.clone(array1)
        joined_list = array1.copy()
        joined_list.extend(array2)
        return joined_list
    
    @staticmethod
    def _copy_list_grow1(array: Optional[List[Any]], new_list_element_type: Optional[Type]) -> List[Any]:
        """
        Returns a copy of the given list of size 1 greater than the argument.
        The last value of the list is left to the default value (None).
        
        Args:
            array: The list to copy, may be None
            new_list_element_type: If array is None, create a size 1 list 
                                   (type is tracked for error simulation)
        
        Returns:
            A new copy of the list of size 1 greater than the input
        """
        if array is not None:
            new_list = array.copy()
            new_list.append(None)
            return new_list
        # Create a new list with one None element
        return [None]
    
    @staticmethod
    def add(array: Optional[List[T]], element: T, expected_type: Optional[Type] = None) -> List[T]:
        if array is not None:
            # preserve existing list elements and inferred component type from array
            inferred_type = type(array[0]) if len(array) > 0 and array[0] is not None else object
        elif element is not None:
            inferred_type = type(element)
        else:
            inferred_type = object

        # If caller provided an expected_type, honor it for validation
        if expected_type is not None:
            # If both array and element are None, we cannot infer a more specific type
            if array is None and element is None:
                if expected_type != object:
                    # Simulate Java ClassCastException by raising TypeError
                    raise TypeError(
                        f"Cannot cast object list to {expected_type.__name__} list (ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.lang.{expected_type.__name__};)"
                    )
            else:
                # If we have an inferred type that is object but expected_type is more specific,
                # and element is not an instance of expected_type (when element present), raise
                if inferred_type is object and element is not None and not isinstance(element, expected_type):
                    raise TypeError(
                        f"Element of type {type(element).__name__} cannot be added to list of {expected_type.__name__}"
                    )

        new_list = ArrayUtils._copy_list_grow1(array, inferred_type)
        new_list[len(new_list) - 1] = element
        return new_list
    
    @staticmethod
    def add_at_index(array: Optional[List[T]], index: int, element: T) -> List[T]:
        """
        Inserts the specified element at the specified position in the list.
        
        Args:
            array: The list to add the element to, may be None
            index: The position of the new object
            element: The object to add
            
        Returns:
            A new list containing the existing elements and the new element
            
        Raises:
            IndexError: If the index is out of range
        """
        if array is None:
            if index != 0:
                raise IndexError(f"Index: {index}, Length: 0")
            return [element]
        
        length = len(array)
        if index > length or index < 0:
            raise IndexError(f"Index: {index}, Length: {length}")
        
        result = array.copy()
        result.insert(index, element)
        return result
    
    # ----------------------------------------------------------------------
    # remove methods
    # ----------------------------------------------------------------------
    
    @staticmethod
    def remove(array: List[T], index: int) -> List[T]:
        """
        Removes the element at the specified position from the specified list.
        
        Args:
            array: The list to remove the element from, may not be None
            index: The position of the element to be removed
            
        Returns:
            A new list containing the existing elements except the element
            at the specified position.
            
        Raises:
            IndexError: If the index is out of range
        """
        if array is None:
            raise IndexError("Cannot remove from None array")
        
        length = len(array)
        if index < 0 or index >= length:
            raise IndexError(f"Index: {index}, Length: {length}")
        
        result = array.copy()
        result.pop(index)
        return result
    
    @staticmethod
    def remove_element(array: Optional[List[T]], element: T) -> Optional[List[T]]:
        """
        Removes the first occurrence of the specified element from the list.
        
        Args:
            array: The list to remove the element from, may be None
            element: The element to be removed
            
        Returns:
            A new list containing the existing elements except the first
            occurrence of the specified element.
        """
        index = ArrayUtils.index_of(array, element)
        if index == ArrayUtils.INDEX_NOT_FOUND:
            return ArrayUtils.clone(array)
        return ArrayUtils.remove(array, index)
    
    # ----------------------------------------------------------------------
    # subarray methods
    # ----------------------------------------------------------------------
    
    @staticmethod
    def subarray(array: Optional[List[T]], start_index_inclusive: int, 
                 end_index_exclusive: int) -> Optional[List[T]]:
        """
        Produces a new list containing the elements between the start and end indices.
        
        Args:
            array: The list
            start_index_inclusive: The starting index (inclusive)
            end_index_exclusive: The ending index (exclusive)
            
        Returns:
            A new list containing the elements between the start and end indices
        """
        if array is None:
            return None
        if start_index_inclusive < 0:
            start_index_inclusive = 0
        if end_index_exclusive > len(array):
            end_index_exclusive = len(array)
        
        new_size = end_index_exclusive - start_index_inclusive
        if new_size <= 0:
            return []
        
        return array[start_index_inclusive:end_index_exclusive]
    
    # ----------------------------------------------------------------------
    # reverse methods
    # ----------------------------------------------------------------------
    
    @staticmethod
    def reverse(array: Optional[List[Any]]) -> None:
        """
        Reverses the order of the given list in-place.
        
        Args:
            array: The list to reverse, may be None
        """
        if array is None:
            return
        array.reverse()
    
    # ----------------------------------------------------------------------
    # isSameLength methods
    # ----------------------------------------------------------------------
    
    @staticmethod
    def is_same_length(array1: Optional[List[Any]], array2: Optional[List[Any]]) -> bool:
        """
        Checks whether two lists are the same length, treating None as length 0.
        
        Args:
            array1: The first list, may be None
            array2: The second list, may be None
            
        Returns:
            True if length of lists matches
        """
        len1 = 0 if array1 is None else len(array1)
        len2 = 0 if array2 is None else len(array2)
        return len1 == len2
    
    # ----------------------------------------------------------------------
    # getLength method
    # ----------------------------------------------------------------------
    
    @staticmethod
    def get_length(array: Optional[List[Any]]) -> int:
        """
        Returns the length of the specified list.
        
        Args:
            array: The list to retrieve the length from, may be None
            
        Returns:
            The length of the list, or 0 if the list is None
        """
        if array is None:
            return 0
        return len(array)

    # ----------------------------------------------------------------------
    # isSameType method
    # ----------------------------------------------------------------------

    @staticmethod
    def is_same_type(array1: Optional[Any], array2: Optional[Any]) -> bool:
        """
        Checks whether two arrays are the same type.
        
        Args:
            array1: The first array, must not be None
            array2: The second array, must not be None
            
        Returns:
            True if type of arrays matches
            
        Raises:
            ValueError: If either array is None
        """
        if array1 is None or array2 is None:
            raise ValueError("The Array must not be null")
        return type(array1) == type(array2)