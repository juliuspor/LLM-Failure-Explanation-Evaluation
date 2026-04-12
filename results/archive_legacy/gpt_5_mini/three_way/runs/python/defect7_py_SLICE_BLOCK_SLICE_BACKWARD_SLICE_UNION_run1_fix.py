# -*- coding: utf-8 -*-
"""
ClassUtils - Utility methods for class operations.

Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import List, Optional, Type, Any, Set
import sys


class ArrayUtils:
    """Utility class for array operations."""
    EMPTY_CLASS_ARRAY: List[Type] = []
    
    @staticmethod
    def is_same_length(array1: Optional[List], array2: Optional[List]) -> bool:
        """Check if two arrays have the same length."""
        len1 = 0 if array1 is None else len(array1)
        len2 = 0 if array2 is None else len(array2)
        return len1 == len2
    
    @staticmethod
    def to_string(array: Optional[List]) -> str:
        """Convert array to string representation."""
        if array is None:
            return "null"
        return str(array)


class StringUtils:
    """Utility class for string operations."""
    EMPTY = ""
    
    @staticmethod
    def delete_whitespace(s: Optional[str]) -> Optional[str]:
        """Delete all whitespace from a string."""
        if s is None:
            return None
        return ''.join(s.split())


class SystemUtils:
    """Utility class for system-related operations."""
    
    @staticmethod
    def is_java_version_at_least(version: float) -> bool:
        """
        Check if Python version is at least the given version.
        Maps to checking Python version >= 3.0 for autoboxing-like behavior.
        """
        # In Python, we always have dynamic typing, so this is always True
        return True


class ClassUtils:
    """
    Operates on classes without using reflection.
    
    This class handles invalid null inputs as best it can.
    Each method documents its behaviour in more detail.
    
    The notion of a canonical name includes the human
    readable name for the type, for example int[]. The
    non-canonical method variants work with the JVM names, such as [I.
    """
    
    # The package separator character: '.'
    PACKAGE_SEPARATOR_CHAR = '.'
    
    # The package separator String: "."
    PACKAGE_SEPARATOR = '.'
    
    # The inner class separator character: '$'
    INNER_CLASS_SEPARATOR_CHAR = '$'
    
    # The inner class separator String: "$"
    INNER_CLASS_SEPARATOR = '$'
    
    # Maps primitive types to wrapper types (Python equivalents)
    _primitive_wrapper_map = {
        bool: bool,
        int: int,
        float: float,
        str: str,
        bytes: bytes,
        type(None): type(None),  # Void.TYPE equivalent
    }
    
    # Maps wrapper types to primitive types
    _wrapper_primitive_map = {}
    
    # Maps primitive class name to abbreviation used in array class names
    _abbreviation_map = {}
    
    # Maps abbreviation to primitive class name
    _reverse_abbreviation_map = {}
    
    @classmethod
    def _init_maps(cls):
        """Initialize the type mapping dictionaries."""
        # Build wrapper to primitive map
        for primitive_class, wrapper_class in cls._primitive_wrapper_map.items():
            if primitive_class != wrapper_class:
                cls._wrapper_primitive_map[wrapper_class] = primitive_class
        
        # Add abbreviations (Java-style)
        cls._add_abbreviation("int", "I")
        cls._add_abbreviation("boolean", "Z")
        cls._add_abbreviation("float", "F")
        cls._add_abbreviation("long", "J")
        cls._add_abbreviation("short", "S")
        cls._add_abbreviation("byte", "B")
        cls._add_abbreviation("double", "D")
        cls._add_abbreviation("char", "C")
    
    @classmethod
    def _add_abbreviation(cls, primitive: str, abbreviation: str):
        """Add primitive type abbreviation to maps."""
        cls._abbreviation_map[primitive] = abbreviation
        cls._reverse_abbreviation_map[abbreviation] = primitive
    
    def __init__(self):
        """
        ClassUtils instances should NOT be constructed in standard programming.
        Instead, the class should be used as ClassUtils.get_short_class_name(cls).
        
        This constructor is public to permit tools that require a JavaBean
        instance to operate.
        """
        pass
    
    # Short class name
    # ----------------------------------------------------------------------
    
    @classmethod
    def get_short_class_name(cls, obj: Any, value_if_null: str = None) -> str:
        """
        Gets the class name minus the package name for an Object.
        
        Args:
            obj: the class to get the short name for, may be None
            value_if_null: the value to return if None
            
        Returns:
            the class name of the object without the package name, or the null value
        """
        if obj is None:
            return value_if_null
        return cls.get_short_class_name_from_class(type(obj))
    
    @classmethod
    def get_short_class_name_from_class(cls, klass: Type) -> str:
        """
        Gets the class name minus the package name from a Class.
        
        Args:
            klass: the class to get the short name for
            
        Returns:
            the class name without the package name or an empty string
        """
        if klass is None:
            return StringUtils.EMPTY
        return cls.get_short_class_name_from_string(klass.__module__ + '.' + klass.__qualname__)
    
    @classmethod
    def get_short_class_name_from_string(cls, class_name: str) -> str:
        """
        Gets the class name minus the package name from a String.
        
        The string passed in is assumed to be a class name - it is not checked.
        
        Args:
            class_name: the className to get the short name for
            
        Returns:
            the class name of the class without the package name or an empty string
        """
        if class_name is None:
            return StringUtils.EMPTY
        if len(class_name) == 0:
            return StringUtils.EMPTY
        
        array_prefix = []
        
        # Handle array encoding
        if class_name.startswith("["):
            while class_name[0] == '[':
                class_name = class_name[1:]
                array_prefix.append("[]")
            # Strip Object type encoding
            if class_name[0] == 'L' and class_name[-1] == ';':
                class_name = class_name[1:-1]
        
        if class_name in cls._reverse_abbreviation_map:
            class_name = cls._reverse_abbreviation_map[class_name]
        
        last_dot_idx = class_name.rfind(cls.PACKAGE_SEPARATOR_CHAR)
        inner_idx = class_name.find(
            cls.INNER_CLASS_SEPARATOR_CHAR, 
            0 if last_dot_idx == -1 else last_dot_idx + 1
        )
        out = class_name[last_dot_idx + 1:]
        if inner_idx != -1:
            out = out.replace(cls.INNER_CLASS_SEPARATOR_CHAR, cls.PACKAGE_SEPARATOR_CHAR)
        return out + ''.join(array_prefix)
    
    # Package name
    # ----------------------------------------------------------------------
    
    @classmethod
    def get_package_name(cls, obj: Any, value_if_null: str = None) -> str:
        """
        Gets the package name of an Object.
        
        Args:
            obj: the class to get the package name for, may be None
            value_if_null: the value to return if None
            
        Returns:
            the package name of the object, or the null value
        """
        if obj is None:
            return value_if_null
        return cls.get_package_name_from_class(type(obj))
    
    @classmethod
    def get_package_name_from_class(cls, klass: Type) -> str:
        """
        Gets the package name of a Class.
        
        Args:
            klass: the class to get the package name for, may be None
            
        Returns:
            the package name or an empty string
        """
        if klass is None:
            return StringUtils.EMPTY
        return cls.get_package_name_from_string(klass.__module__ + '.' + klass.__qualname__)
    
    @classmethod
    def get_package_name_from_string(cls, class_name: str) -> str:
        """
        Gets the package name from a String.
        
        The string passed in is assumed to be a class name - it is not checked.
        If the class is unpackaged, return an empty string.
        
        Args:
            class_name: the className to get the package name for, may be None
            
        Returns:
            the package name or an empty string
        """
        if class_name is None or len(class_name) == 0:
            return StringUtils.EMPTY
        
        # Strip array encoding
        while class_name[0] == '[':
            class_name = class_name[1:]
        # Strip Object type encoding
        if class_name[0] == 'L' and class_name[-1] == ';':
            class_name = class_name[1:]
        
        i = class_name.rfind(cls.PACKAGE_SEPARATOR_CHAR)
        if i == -1:
            return StringUtils.EMPTY
        return class_name[:i]
    
    # Superclasses/Superinterfaces
    # ----------------------------------------------------------------------
    
    @classmethod
    def get_all_superclasses(cls, klass: Type) -> Optional[List[Type]]:
        """
        Gets a List of superclasses for the given class.
        
        Args:
            klass: the class to look up, may be None
            
        Returns:
            the List of superclasses in order going up from this one,
            None if None input
        """
        if klass is None:
            return None
        classes = []
        superclass = klass.__bases__[0] if klass.__bases__ else None
        while superclass is not None and superclass != object:
            classes.append(superclass)
            superclass = superclass.__bases__[0] if superclass.__bases__ else None
        return classes
    
    @classmethod
    def get_all_interfaces(cls, klass: Type) -> Optional[List[Type]]:
        """
        Gets a List of all interfaces implemented by the given class and its superclasses.
        
        The order is determined by looking through each interface in turn as
        declared in the source file and following its hierarchy up. Then each
        superclass is considered in the same way. Later duplicates are ignored,
        so the order is maintained.
        
        Args:
            klass: the class to look up, may be None
            
        Returns:
            the List of interfaces in order, None if None input
        """
        if klass is None:
            return None
        
        interfaces_found: Set[Type] = set()
        cls._get_all_interfaces(klass, interfaces_found)
        
        return list(interfaces_found)
    
    @classmethod
    def _get_all_interfaces(cls, klass: Type, interfaces_found: Set[Type]):
        """
        Get the interfaces for the specified class.
        
        Args:
            klass: the class to look up, may be None
            interfaces_found: the Set of interfaces for the class
        """
        while klass is not None:
            interfaces = klass.__bases__
            
            for i in interfaces:
                if i != object and i not in interfaces_found:
                    interfaces_found.add(i)
                    cls._get_all_interfaces(i, interfaces_found)
            
            # Move to superclass
            klass = klass.__bases__[0] if klass.__bases__ and klass.__bases__[0] != object else None
    
    # Convert list
    # ----------------------------------------------------------------------
    
    @classmethod
    def convert_class_names_to_classes(cls, class_names: Optional[List[str]]) -> Optional[List[Optional[Type]]]:
        """
        Given a List of class names, this method converts them into classes.
        
        A new List is returned. If the class name cannot be found, None
        is stored in the List. If the class name in the List is
        None, None is stored in the output List.
        
        Args:
            class_names: the classNames to change
            
        Returns:
            a List of Class objects corresponding to the class names,
            None if None input
        """
        if class_names is None:
            return None
        classes = []
        for class_name in class_names:
            try:
                # Attempt to import and get class
                if class_name is None:
                    classes.append(None)
                else:
                    # Try to get built-in type or import module
                    if '.' in class_name:
                        module_name, cls_name = class_name.rsplit('.', 1)
                        module = __import__(module_name, fromlist=[cls_name])
                        classes.append(getattr(module, cls_name))
                    else:
                        # Try built-ins
                        classes.append(eval(class_name))
            except Exception:
                classes.append(None)
        return classes
    
    @classmethod
    def convert_classes_to_class_names(cls, classes: Optional[List[Optional[Type]]]) -> Optional[List[Optional[str]]]:
        """
        Given a List of Class objects, this method converts them into class names.
        
        A new List is returned. None objects will be copied into
        the returned list as None.
        
        Args:
            classes: the classes to change
            
        Returns:
            a List of class names corresponding to the Class objects,
            None if None input
        """
        if classes is None:
            return None
        class_names = []
        for klass in classes:
            if klass is None:
                class_names.append(None)
            else:
                class_names.append(klass.__module__ + '.' + klass.__qualname__)
        return class_names
    
    # Is assignable
    # ----------------------------------------------------------------------
    
    @classmethod
    def is_assignable_array(cls, class_array: Optional[List[Type]], 
                            to_class_array: Optional[List[Type]],
                            autoboxing: bool = None) -> bool:
        """
        Checks if an array of Classes can be assigned to another array of Classes.
        
        This method calls is_assignable for each Class pair in the input arrays.
        It can be used to check if a set of arguments (the first parameter) are
        suitably compatible with a set of method parameter types (the second parameter).
        
        Args:
            class_array: the array of Classes to check, may be None
            to_class_array: the array of Classes to try to assign into, may be None
            autoboxing: whether to use implicit autoboxing/unboxing between primitives and wrappers
            
        Returns:
            True if assignment possible
        """
        if autoboxing is None:
            autoboxing = SystemUtils.is_java_version_at_least(1.5)
        
        if not ArrayUtils.is_same_length(class_array, to_class_array):
            return False
        if class_array is None:
            class_array = ArrayUtils.EMPTY_CLASS_ARRAY
        if to_class_array is None:
            to_class_array = ArrayUtils.EMPTY_CLASS_ARRAY
        for i in range(len(class_array)):
            if not cls.is_assignable(class_array[i], to_class_array[i], autoboxing):
                return False
        return True
    
    @classmethod
    def is_assignable(cls, klass: Type, to_class: Type, autoboxing: bool = None) -> bool:
        """
        Checks if one Class can be assigned to a variable of another Class.
        
        Unlike the issubclass() function, this method takes into account
        None values.
        
        None may be assigned to any reference type. This method
        will return True if None is passed in and the to_class is
        not a primitive type.
        
        Args:
            klass: the Class to check, may be None
            to_class: the Class to try to assign into, returns False if None
            autoboxing: whether to use implicit autoboxing/unboxing
            
        Returns:
            True if assignment possible
        """
        if autoboxing is None:
            autoboxing = SystemUtils.is_java_version_at_least(1.5)
        
        if to_class is None:
            return False
        # Have to check for None, as issubclass doesn't handle it
        if klass is None:
            return True  # None can be assigned to any reference type in Python
        
        # In Python, we don't have true primitives, but we simulate the behavior
        if autoboxing:
            if klass in cls._primitive_wrapper_map:
                klass = cls.primitive_to_wrapper(klass)
                if klass is None:
                    return False
            if to_class in cls._wrapper_primitive_map:
                klass = cls.wrapper_to_primitive(klass)
                if klass is None:
                    return False
        
        if klass == to_class:
            return True
        
        # Check if klass is subclass of to_class
        try:
            return issubclass(klass, to_class)
        except TypeError:
            return False
    
    @classmethod
    def primitive_to_wrapper(cls, klass: Type) -> Type:
        """
        Converts the specified primitive Class object to its corresponding
        wrapper Class object.
        
        Args:
            klass: the class to convert, may be None
            
        Returns:
            the wrapper class for klass or klass if klass is not a primitive.
            None if None input.
        """
        converted_class = klass
        if klass is not None and klass in cls._primitive_wrapper_map:
            converted_class = cls._primitive_wrapper_map.get(klass)
        return converted_class
    
    @classmethod
    def primitives_to_wrappers(cls, classes: Optional[List[Type]]) -> Optional[List[Type]]:
        """
        Converts the specified array of primitive Class objects to an array of
        its corresponding wrapper Class objects.
        
        Args:
            classes: the class array to convert, may be None or empty
            
        Returns:
            an array which contains for each given class, the wrapper class or
            the original class if class is not a primitive. None if None input.
            Empty array if an empty array passed in.
        """
        if classes is None:
            return None
        
        if len(classes) == 0:
            return classes
        
        converted_classes = []
        for i in range(len(classes)):
            converted_classes.append(cls.primitive_to_wrapper(classes[i]))
        return converted_classes
    
    @classmethod
    def wrapper_to_primitive(cls, klass: Type) -> Optional[Type]:
        """
        Converts the specified wrapper class to its corresponding primitive class.
        
        This method is the counter part of primitive_to_wrapper().
        If the passed in class is a wrapper class for a primitive type, this
        primitive type will be returned. For other classes, or if the parameter is
        None, the return value is None.
        
        Args:
            klass: the class to convert, may be None
            
        Returns:
            the corresponding primitive type if klass is a wrapper class, None otherwise
        """
        return cls._wrapper_primitive_map.get(klass)
    
    @classmethod
    def wrappers_to_primitives(cls, classes: Optional[List[Type]]) -> Optional[List[Optional[Type]]]:
        """
        Converts the specified array of wrapper Class objects to an array of
        its corresponding primitive Class objects.
        
        This method invokes wrapper_to_primitive() for each element
        of the passed in array.
        
        Args:
            classes: the class array to convert, may be None or empty
            
        Returns:
            an array which contains for each given class, the primitive class or
            None if the original class is not a wrapper class. None if None input.
            Empty array if an empty array passed in.
        """
        if classes is None:
            return None
        
        if len(classes) == 0:
            return classes
        
        converted_classes = []
        for i in range(len(classes)):
            converted_classes.append(cls.wrapper_to_primitive(classes[i]))
        return converted_classes
    
    # Inner class
    # ----------------------------------------------------------------------
    
    @classmethod
    def is_inner_class(cls, klass: Type) -> bool:
        """
        Is the specified class an inner class or static nested class.
        
        Args:
            klass: the class to check, may be None
            
        Returns:
            True if the class is an inner or static nested class,
            False if not or None
        """
        if klass is None:
            return False
        return cls.INNER_CLASS_SEPARATOR_CHAR in klass.__qualname__
    
    # Class loading
    # ----------------------------------------------------------------------
    
    @classmethod
    def get_class(cls, class_name: str, initialize: bool = True) -> Type:
        """
        Returns the class represented by class_name using the
        current module context. This implementation supports names like
        "module.ClassName" as well as built-in type names.
        
        Args:
            class_name: the class name
            initialize: whether the class must be initialized (not used in Python)
            
        Returns:
            the class represented by class_name
            
        Raises:
            ImportError: if the class is not found
        """
        class_name = cls._to_canonical_name(class_name)
        
        if class_name in cls._abbreviation_map:
            # Handle primitive type abbreviations
            cls_name = "[" + cls._abbreviation_map[class_name]
            # Return the component type (simulated)
            return eval(class_name)
        else:
            # Try to import module and get class
            if '.' in class_name:
                module_name, cls_name = class_name.rsplit('.', 1)
                module = __import__(module_name, fromlist=[cls_name])
                return getattr(module, cls_name)
            else:
                # Try built-ins
                return eval(class_name)
    
    @classmethod
    def get_class_with_loader(cls, class_loader: Any, class_name: str, initialize: bool = True) -> Type:
        """
        Returns the class represented by class_name using the specified loader.
        
        Args:
            class_loader: the class loader to use (not used in Python)
            class_name: the class name
            initialize: whether the class must be initialized
            
        Returns:
            the class represented by class_name
            
        Raises:
            ImportError: if the class is not found
        """
        return cls.get_class(class_name, initialize)
    
    # Public method
    # ----------------------------------------------------------------------
    
    @classmethod
    def get_public_method(cls, klass: Type, method_name: str, 
                          parameter_types: List[Type] = None) -> Any:
        """
        Returns the desired Method much like getattr, however
        it ensures that the returned Method is from a public class or interface.
        
        Args:
            klass: the class to check, not None
            method_name: the name of the method
            parameter_types: the list of parameters (not used in Python)
            
        Returns:
            the method
            
        Raises:
            AttributeError: if the method is not found
            TypeError: if the class is None
        """
        if klass is None:
            raise TypeError("klass must not be None")
        
        declared_method = getattr(klass, method_name, None)
        if declared_method is not None:
            return declared_method
        
        # Search in interfaces and superclasses
        candidate_classes = []
        interfaces = cls.get_all_interfaces(klass)
        if interfaces:
            candidate_classes.extend(interfaces)
        superclasses = cls.get_all_superclasses(klass)
        if superclasses:
            candidate_classes.extend(superclasses)
        
        for candidate_class in candidate_classes:
            candidate_method = getattr(candidate_class, method_name, None)
            if candidate_method is not None:
                return candidate_method
        
        raise AttributeError(f"Can't find a public method for {method_name} {ArrayUtils.to_string(parameter_types)}")
    
    # ----------------------------------------------------------------------
    
    @classmethod
    def _to_canonical_name(cls, class_name: str) -> str:
        """
        Converts a class name to a JLS style class name.
        
        Args:
            class_name: the class name
            
        Returns:
            the converted name
        """
        class_name = StringUtils.delete_whitespace(class_name)
        if class_name is None:
            raise ValueError("class_name must not be None.")
        elif class_name.endswith("[]"):
            class_name_buffer = []
            while class_name.endswith("[]"):
                class_name = class_name[:-2]
                class_name_buffer.append("[")
            abbreviation = cls._abbreviation_map.get(class_name)
            if abbreviation is not None:
                class_name_buffer.append(abbreviation)
            else:
                class_name_buffer.append("L")
                class_name_buffer.append(class_name)
                class_name_buffer.append(";")
            class_name = ''.join(class_name_buffer)
        return class_name
    
    @classmethod
    def to_class(cls, array: Optional[List[Any]]) -> Optional[List[Type]]:
        if array is None:
            return None
        elif len(array) == 0:
            return ArrayUtils.EMPTY_CLASS_ARRAY.copy()
        classes = []
        for item in array:
            if item is None:
                raise AttributeError("Array element is None")
            classes.append(type(item))
        return classes
    
    # Short canonical name
    # ----------------------------------------------------------------------
    
    @classmethod
    def get_short_canonical_name(cls, obj: Any, value_if_null: str = None) -> str:
        """
        Gets the canonical name minus the package name for an Object.
        
        Args:
            obj: the class to get the short name for, may be None
            value_if_null: the value to return if None
            
        Returns:
            the canonical name of the object without the package name, or the null value
        """
        if obj is None:
            return value_if_null
        return cls.get_short_canonical_name_from_string(type(obj).__module__ + '.' + type(obj).__qualname__)
    
    @classmethod
    def get_short_canonical_name_from_class(cls, klass: Type) -> str:
        """
        Gets the canonical name minus the package name from a Class.
        
        Args:
            klass: the class to get the short name for
            
        Returns:
            the canonical name without the package name or an empty string
        """
        if klass is None:
            return StringUtils.EMPTY
        return cls.get_short_canonical_name_from_string(klass.__module__ + '.' + klass.__qualname__)
    
    @classmethod
    def get_short_canonical_name_from_string(cls, canonical_name: str) -> str:
        """
        Gets the canonical name minus the package name from a String.
        
        The string passed in is assumed to be a canonical name - it is not checked.
        
        Args:
            canonical_name: the class name to get the short name for
            
        Returns:
            the canonical name of the class without the package name or an empty string
        """
        return cls.get_short_class_name_from_string(cls._get_canonical_name(canonical_name))
    
    # Package name
    # ----------------------------------------------------------------------
    
    @classmethod
    def get_package_canonical_name(cls, obj: Any, value_if_null: str = None) -> str:
        """
        Gets the package name from the canonical name of an Object.
        
        Args:
            obj: the class to get the package name for, may be None
            value_if_null: the value to return if None
            
        Returns:
            the package name of the object, or the null value
        """
        if obj is None:
            return value_if_null
        return cls.get_package_canonical_name_from_string(type(obj).__module__ + '.' + type(obj).__qualname__)
    
    @classmethod
    def get_package_canonical_name_from_class(cls, klass: Type) -> str:
        """
        Gets the package name from the canonical name of a Class.
        
        Args:
            klass: the class to get the package name for, may be None
            
        Returns:
            the package name or an empty string
        """
        if klass is None:
            return StringUtils.EMPTY
        return cls.get_package_canonical_name_from_string(klass.__module__ + '.' + klass.__qualname__)
    
    @classmethod
    def get_package_canonical_name_from_string(cls, canonical_name: str) -> str:
        """
        Gets the package name from the canonical name.
        
        The string passed in is assumed to be a canonical name - it is not checked.
        If the class is unpackaged, return an empty string.
        
        Args:
            canonical_name: the canonical name to get the package name for, may be None
            
        Returns:
            the package name or an empty string
        """
        return cls.get_package_name_from_string(cls._get_canonical_name(canonical_name))
    
    @classmethod
    def _get_canonical_name(cls, class_name: str) -> Optional[str]:
        """
        Converts a given name of class into canonical format.
        If name of class is not a name of array class it returns
        unchanged name.
        
        Example:
            _get_canonical_name("[I") = "int[]"
            _get_canonical_name("[Ljava.lang.String;") = "java.lang.String[]"
            _get_canonical_name("java.lang.String") = "java.lang.String"
        
        Args:
            class_name: the name of class
            
        Returns:
            canonical form of class name
        """
        class_name = StringUtils.delete_whitespace(class_name)
        if class_name is None:
            return None
        else:
            dim = 0
            while class_name.startswith("["):
                dim += 1
                class_name = class_name[1:]
            if dim < 1:
                return class_name
            else:
                if class_name.startswith("L"):
                    class_name = class_name[1:len(class_name) - 1 if class_name.endswith(";") else len(class_name)]
                else:
                    if len(class_name) > 0:
                        class_name = cls._reverse_abbreviation_map.get(class_name[0:1], class_name)
                canonical_class_name_buffer = [class_name]
                for i in range(dim):
                    canonical_class_name_buffer.append("[]")
                return ''.join(canonical_class_name_buffer)


# Initialize the maps when module is loaded
ClassUtils._init_maps()