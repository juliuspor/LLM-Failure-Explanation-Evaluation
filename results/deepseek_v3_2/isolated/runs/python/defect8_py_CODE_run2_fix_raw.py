    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length == 2:
            # Language only
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        
        # Must have at least 5 characters: aa_BB
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check first two letters (language)
        if not ('a' <= locale_str[0] <= 'z' and 'a' <= locale_str[1] <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check next two letters (country) are uppercase
        if not ('A' <= locale_str[3] <= 'Z' and 'A' <= locale_str[4] <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # Must have at least 7 characters for variant: aa_BB_v
        if length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check second underscore
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Variant is everything after the second underscore
        variant = locale_str[6:]
        if not variant:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(locale_str[0:2], locale_str[3:5], variant)