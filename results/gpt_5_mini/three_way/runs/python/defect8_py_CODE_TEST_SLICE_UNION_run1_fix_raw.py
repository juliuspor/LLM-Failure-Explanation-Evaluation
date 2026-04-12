@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if not (length == 2 or length == 5 or length >= 7):
            raise ValueError(f"Invalid locale format: {locale_str}")
        # language must be two lowercase letters
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # must have separator at index 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # At this point, length is >=5 or >=7. For length >=5, positions 3 and 4 may be letters or underscores (empty country)
        # Handle empty country (double underscore) where locale like 'fr__POSIX' -> country is '' and variant is from index 3? Actually pattern is 'll_CC_variant' or 'll__variant'
        # For standard parsing, expect either two uppercase letters at 3-4, or underscore at 3 indicating empty country (i.e., locale_str[3]=='_' and then variant begins at 4 or 5)
        # We'll follow Java behavior: after 'll_' then either 'CC' (two uppercase) or '_' then variant starts at index 3+1? In examples 'fr__POSIX' has '_' at 2 and 3, variant starts at 4.
        # So check for underscore at index 3 meaning empty country
        if length >= 5:
            ch3 = locale_str[3]
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if ch3 == '_':
            # empty country, variant is the rest after index 3 (i.e., from 4)
            # In form 'll__variant', variant starts at index 4
            if length == 4:
                # 'll__' with nothing after
                return Locale(locale_str[0:2], "", "")
            # variant should start at index 4
            variant = locale_str[4:]
            return Locale(locale_str[0:2], "", variant)
        else:
            # Expect two uppercase letters at 3 and 4
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            # length >=7, expect '_' at index 5
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            return Locale(locale_str[0:2], locale_str[3:5], variant)