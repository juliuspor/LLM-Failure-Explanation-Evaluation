@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # Minimum 2 (language), or patterns like ll_CC or ll__VARIANT or ll_CC_VAR
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Validate language (first two chars)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # Must have separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Split into parts with at most 3 components
        parts = locale_str.split('_', 2)
        # parts[0] is language
        # Possible forms:
        # ['ll', 'CC'] -> but split with max 2 will give ['ll', 'CC']? Actually with maxsplit=2, 'en_GB' -> ['en','GB']
        # For consistency handle lengths
        if len(parts) == 2:
            # form ll_V where V could be country (2 uppercase) or variant (if country missing?)
            mid = parts[1]
            # If mid is length 2, treat as country
            if len(mid) == 2:
                ch3 = mid[0]
                ch4 = mid[1]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(parts[0], mid)
            # Otherwise treat as variant with empty country
            if len(mid) == 0:
                return Locale(parts[0], "")
            # variant (country empty)
            return Locale(parts[0], "", mid)
        else:
            # len(parts) == 3 -> ll_CC_VAR or ll__VAR
            country = parts[1]
            variant = parts[2]
            if len(country) == 0:
                # allow empty country with non-empty variant
                if len(variant) == 0:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(parts[0], "", variant)
            # validate country length and casing
            if len(country) != 2:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = country[0]
            ch4 = country[1]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(variant) == 0:
                return Locale(parts[0], country)
            return Locale(parts[0], country, variant)