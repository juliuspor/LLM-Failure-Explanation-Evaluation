    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least '_' after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, only language and underscore (e.g., "fr_")
        if length == 3:
            return Locale(locale_str[0:2], "")
        
        # Find the next underscore after position 2
        next_underscore = locale_str.find('_', 3)
        
        if next_underscore == -1:
            # No second underscore, entire remainder is country
            country_part = locale_str[3:]
            if len(country_part) == 2:
                # Validate country code is two uppercase letters
                if country_part[0] < 'A' or country_part[0] > 'Z' or country_part[1] < 'A' or country_part[1] > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], country_part)
            else:
                # Allow non‑standard country codes (e.g., numeric)
                return Locale(locale_str[0:2], country_part)
        else:
            # There is a second underscore
            country_part = locale_str[3:next_underscore]
            variant_part = locale_str[next_underscore + 1:]
            
            # Validate country part if it is exactly two uppercase letters
            if len(country_part) == 2:
                if country_part[0] < 'A' or country_part[0] > 'Z' or country_part[1] < 'A' or country_part[1] > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
            # If country part is empty (double underscore), treat as no country
            if country_part == "":
                return Locale(locale_str[0:2], "", variant_part)
            else:
                return Locale(locale_str[0:2], country_part, variant_part)