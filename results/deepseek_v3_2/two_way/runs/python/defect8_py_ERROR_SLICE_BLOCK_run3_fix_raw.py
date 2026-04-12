    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Handle special case for POSIX locale
        if locale_str.endswith('_POSIX'):
            # Check if it's a valid language code followed by '__POSIX'
            # e.g., 'fr__POSIX' -> language='fr', country='', variant='POSIX'
            # The format is language + '__' + 'POSIX' (double underscore)
            # We'll split on double underscore
            if '__' in locale_str:
                lang_part, variant_part = locale_str.split('__', 1)
                if len(lang_part) == 2 and lang_part.isalpha() and lang_part.islower():
                    return Locale(lang_part, '', variant_part)
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
        
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
            
            # For length >= 5, check if we have a country code
            if length >= 5:
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    # Might be a variant without country, e.g., 'fr__POSIX' already handled above
                    # But also could be like 'fr_xxx' where xxx is variant
                    # Actually, if ch3 and ch4 are not uppercase letters, then we might have
                    # a variant directly after language, like 'fr_xxx' (where xxx is variant)
                    # In that case, country is empty, variant is the part after first underscore
                    # However, the standard format expects country code (2 uppercase) or nothing.
                    # We'll allow variant without country: language + '_' + variant
                    # But only if we haven't already handled the POSIX case.
                    # So we need to check if after the first underscore we have something
                    # that is not a valid country code.
                    # Let's assume that if the third character is not uppercase, then it's a variant.
                    # But we must ensure the variant part is not empty.
                    if length > 3:
                        # There is at least one character after the underscore
                        # So country is empty, variant is everything after the first underscore
                        return Locale(locale_str[0:2], "", locale_str[3:])
                    else:
                        raise ValueError(f"Invalid locale format: {locale_str}")
                
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            else:
                # length is 3 or 4? Actually, we already checked length !=2 and length !=5 and length <7
                # So length could be 3 or 4. But we already checked that length <7 and not 2,5.
                # So length could be 3,4,6, or >=7. But we are in else branch (length !=2).
                # We already checked length >=5? Actually, we have if length >=5 above.
                # So if length is 3 or 4, we fall here.
                # For length 3 or 4, we have language + '_' + something (maybe variant)
                # Example: 'fr_xxx' where xxx is variant of length 3.
                # So we treat country as empty, variant as everything after first underscore.
                if length > 3:
                    return Locale(locale_str[0:2], "", locale_str[3:])
                else:
                    # length == 3: language + '_' + single character? That's unusual but maybe allowed.
                    return Locale(locale_str[0:2], "", locale_str[3:])