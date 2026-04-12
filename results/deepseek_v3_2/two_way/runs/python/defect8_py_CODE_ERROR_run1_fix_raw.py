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
        
        # Must have at least 5 characters for language_country
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check for first underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate country code (two uppercase letters)
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # Handle variant: there must be an underscore separator after country
        # The separator can be a single underscore (at index 5) or double underscore (at indices 5 and 6?)
        # Actually, the variant separator is a single underscore, but the variant itself may be empty?
        # In Java Locale, the variant is separated by a single underscore, but the string representation
        # for POSIX is "fr__POSIX" (double underscore) because the country is empty.
        # The issue is that the original code assumed country is always present when variant is present.
        # But in "fr__POSIX", the country is empty, so the format is language + "__" + variant.
        # We need to handle the case where after the first underscore, we might have another underscore
        # indicating empty country.
        
        # Check if the character at index 5 is '_' (separator for variant)
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 6 characters: "fr__PO" (for "fr__POSIX")
        # If the country is empty, then the variant starts at index 6? Actually, in "fr__POSIX":
        # indices: 0=f,1=r,2=_,3=_,4=P,5=O,6=S,7=I,8=X
        # So after the first underscore (index2), we have another underscore (index3) because country is empty.
        # The original code expected country at indices 3 and 4, but here index3 is '_' and index4 is 'P'.
        # That's why the validation of country fails. We need to detect empty country.
        
        # Let's re-express: The locale string can be:
        # 1. language (2 chars)
        # 2. language + "_" + country (5 chars)
        # 3. language + "_" + country + "_" + variant (>=7 chars)
        # 4. language + "_" + "_" + variant (>=6 chars)  [empty country]
        # The original code only handled cases 1,2,3 but not case 4.
        
        # So we need to check if after the first underscore, the next two characters are uppercase letters (country)
        # or if the next character is another underscore (empty country).
        
        # Actually, we already validated ch3 and ch4 as uppercase letters. That assumes country is present.
        # But for "fr__POSIX", ch3 is '_' (not uppercase), so the validation fails earlier.
        # We need to adjust the logic to allow empty country.
        
        # Let's restructure:
        # After validating language and first underscore, we look at the next segment.
        # If the next character is '_' (i.e., locale_str[3] == '_'), then country is empty and variant starts at index 4.
        # Otherwise, we expect two uppercase letters for country.
        
        # But note: the original code already validated ch3 and ch4 as uppercase for length >=5.
        # We need to change that validation to conditionally check for country only if not empty.
        
        # Revised approach:
        # After checking first underscore at index2:
        # If length == 3: invalid (just language_)
        # If locale_str[3] == '_': empty country
        # else: country is two uppercase letters.
        
        # However, the original code assumed length >=5 for country. We need to handle length >=3.
        
        # Let's rewrite the function from scratch to handle all cases:
        # 1. length == 2: language only
        # 2. length >= 3: must have '_' at index2
        #   2a. if length == 3: invalid (trailing underscore)
        #   2b. if locale_str[3] == '_': empty country, variant starts at index4
        #   2c. else: country is two uppercase letters at indices 3 and 4, then optionally '_' + variant
        
        # But we must maintain compatibility with existing tests and Java's Locale.toString() format.
        # Java's Locale.toString() returns:
        # - language
        # - language + "_" + country
        # - language + "_" + country + "_" + variant
        # - language + "_" + "_" + variant (if country empty)
        
        # So we implement accordingly.
        
        # Let's implement step by step:
        
        # We already handled length==2.
        # Now length>=3.
        
        # Check first underscore
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length == 3, invalid because just "fr_"
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check second character after language underscore
        if locale_str[3] == '_':
            # Empty country: format language + "__" + variant
            country = ""
            variant_start = 4
        else:
            # Country expected
            if length < 5:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = locale_str[3:5]
            variant_start = 5
        
        # Now check for variant
        if length > variant_start:
            # There is more string after country (or after empty country)
            # Check for variant separator underscore
            if locale_str[variant_start] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[variant_start+1:]
        else:
            variant = ""
        
        return Locale(locale_str[0:2], country, variant)
