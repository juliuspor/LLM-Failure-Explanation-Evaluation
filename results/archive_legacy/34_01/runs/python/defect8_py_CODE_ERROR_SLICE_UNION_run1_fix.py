@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        """
        Converts a String to a Locale.

        This method takes the string format of a locale and creates the
        locale object from it.

        Examples:
            LocaleUtils.to_locale("en")         = Locale("en", "")
            LocaleUtils.to_locale("en_GB")      = Locale("en", "GB")
            LocaleUtils.to_locale("en_GB_xxx")  = Locale("en", "GB", "xxx")   (#)

        (#) The behaviour of the JDK variant constructor changed between JDK1.3 and JDK1.4.
        In JDK1.3, the constructor upper cases the variant, in JDK1.4, it doesn't.
        Thus, the result from get_variant() may vary depending on your JDK.

        This method validates the input strictly.
        The language code must be lowercase.
        The country code must be uppercase.
        The separator must be an underscore.
        The length must be correct.

        Args:
            locale_str: the locale String to convert, None returns None
            
        Returns:
            a Locale, None if None input
            
        Raises:
            ValueError: if the string is an invalid format
        """
        if locale_str is None:
            return None
        length = len(locale_str)
        if length != 2 and length != 5 and length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        else:
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if locale_str[3] == '_':
                return Locale(locale_str[0:2], "", locale_str[4:])
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])