    @classmethod
    def to_locale(cls, locale_str: str) -> Locale:
        """
        Converts a string to a Locale.

        This method takes the string format of a locale and creates the
        locale object from it.

        Args:
            locale_str: the locale string to convert, null returns null

        Returns:
            the Locale object, or null if the input was null
        """
        if locale_str is None:
            return None
        if len(locale_str) == 0:
            raise ValueError("Invalid locale format: " + locale_str)
        
        length = len(locale_str)
        if length != 2 and length != 5 and length < 7:
            raise ValueError("Invalid locale format: " + locale_str)
        
        if length == 2:
            return Locale(locale_str, "")
        else:
            # length is 5 or >=7, must have '_' at position 2
            if locale_str[2] != '_':
                raise ValueError("Invalid locale format: " + locale_str)
            
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError("Invalid locale format: " + locale_str)
            
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # length >=7, must have '_' at position 5
                if locale_str[5] != '_':
                    raise ValueError("Invalid locale format: " + locale_str)
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
