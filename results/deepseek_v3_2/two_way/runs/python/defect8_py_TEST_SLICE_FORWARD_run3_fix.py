# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
LocaleUtils - Operations to assist when working with a Locale.

This class tries to handle None input gracefully.
An exception will not be thrown for a None input.
Each method documents its behaviour in more detail.
"""

from typing import List, Optional, Set, Dict, FrozenSet
from threading import Lock


class Locale:
    """
    Represents a locale (language, country, variant).
    Equivalent to Java's java.util.Locale.
    """
    
    def __init__(self, language: str, country: str = "", variant: str = ""):
        """
        Construct a locale from language, country and variant.
        
        Args:
            language: An ISO 639 alpha-2 or alpha-3 language code
            country: An ISO 3166 alpha-2 country code or UN M.49 numeric-3 area code
            variant: Any arbitrary value used to indicate a variation of a Locale
        """
        self._language = language.lower() if language else ""
        self._country = country.upper() if country else ""
        self._variant = variant if variant else ""
    
    def get_language(self) -> str:
        """Returns the language code of this Locale."""
        return self._language
    
    def get_country(self) -> str:
        """Returns the country/region code for this locale."""
        return self._country
    
    def get_variant(self) -> str:
        """Returns the variant code for this locale."""
        return self._variant
    
    # Property aliases for Pythonic access
    @property
    def language(self) -> str:
        return self._language
    
    @property
    def country(self) -> str:
        return self._country
    
    @property
    def variant(self) -> str:
        return self._variant
    
    def __str__(self) -> str:
        """Returns a string representation of this Locale."""
        result = self._language
        if self._country:
            result += "_" + self._country
        if self._variant:
            if not self._country:
                result += "_"  # Empty country, but variant exists
            result += "_" + self._variant
        return result
    
    def __repr__(self) -> str:
        return f"Locale('{self._language}', '{self._country}', '{self._variant}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Locale):
            return False
        return (self._language == other._language and 
                self._country == other._country and 
                self._variant == other._variant)
    
    def __hash__(self) -> int:
        return hash((self._language, self._country, self._variant))
    
    @classmethod
    def get_available_locales(cls) -> List['Locale']:
        """
        Returns an array of all installed locales.
        Equivalent to Java's Locale.getAvailableLocales().
        
        Returns:
            An array of installed locales.
        """
        # Simulated available locales (in Java, this comes from the JVM)
        return [
            Locale("en", "US"),
            Locale("en", "GB"),
            Locale("en", "CA"),
            Locale("en", "AU"),
            Locale("fr", "FR"),
            Locale("fr", "CA"),
            Locale("fr", "BE"),
            Locale("de", "DE"),
            Locale("de", "AT"),
            Locale("de", "CH"),
            Locale("es", "ES"),
            Locale("es", "MX"),
            Locale("it", "IT"),
            Locale("pt", "BR"),
            Locale("pt", "PT"),
            Locale("ja", "JP"),
            Locale("zh", "CN"),
            Locale("zh", "TW"),
            Locale("ko", "KR"),
            Locale("ru", "RU"),
            Locale("en"),
            Locale("fr"),
            Locale("de"),
            Locale("es"),
            Locale("it"),
            Locale("pt"),
            Locale("ja"),
            Locale("zh"),
            Locale("ko"),
            Locale("ru"),
        ]


class LocaleUtils:
    """
    Operations to assist when working with a Locale.

    This class tries to handle None input gracefully.
    An exception will not be thrown for a None input.
    Each method documents its behaviour in more detail.
    
    @author Stephen Colebourne
    @since 2.2
    """
    
    # Unmodifiable list of available locales.
    _c_available_locale_list: List[Locale] = None
    
    # Unmodifiable set of available locales.
    _c_available_locale_set: FrozenSet[Locale] = None
    
    # Unmodifiable map of language locales by country. (synchronized)
    _c_languages_by_country: Dict[str, List[Locale]] = {}
    _languages_by_country_lock = Lock()
    
    # Unmodifiable map of country locales by language. (synchronized)
    _c_countries_by_language: Dict[str, List[Locale]] = {}
    _countries_by_language_lock = Lock()
    
    # Static initialization block equivalent
    @classmethod
    def _ensure_initialized(cls):
        """Static initialization block equivalent - initializes the available locale list."""
        if cls._c_available_locale_list is None:
            locale_list = list(Locale.get_available_locales())
            cls._c_available_locale_list = tuple(locale_list)  # Unmodifiable (tuple)
    
    def __init__(self):
        """
        LocaleUtils instances should NOT be constructed in standard programming.
        Instead, the class should be used as LocaleUtils.to_locale("en_GB").

        This constructor is public to permit tools that require a JavaBean instance
        to operate.
        """
        super().__init__()
    
    # -----------------------------------------------------------------------
    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        # Split by underscore, but handle consecutive underscores as empty parts
        parts = locale_str.split('_')
        # Reconstruct parts to handle empty strings correctly
        # For example, 'fr__POSIX' -> ['fr', '', 'POSIX']
        # However, split('_') on 'fr__POSIX' gives ['fr', '', 'POSIX']
        # But for 'en_GB' -> ['en', 'GB']
        # For 'en_GB_xxx' -> ['en', 'GB', 'xxx']
        # For 'en' -> ['en']

        # Validate that we have between 1 and 3 parts after split
        if len(parts) < 1 or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")

        language = parts[0]
        country = ""
        variant = ""

        if len(parts) >= 2:
            # The second part could be country or variant if empty country
            if parts[1] == "":
                # This means we have two underscores in a row: language__variant
                # So parts[1] is empty, parts[2] is variant
                if len(parts) == 3:
                    variant = parts[2]
                else:
                    # Actually, if we have only two parts and the second is empty,
                    # that would be like 'fr__' which is invalid because variant missing.
                    # But we'll let validation handle.
                    pass
            else:
                # Second part is non-empty: could be country or variant if only two parts?
                # According to Java locale format, if there are two parts, the second is country.
                # If there are three parts, second is country, third is variant.
                # However, we also need to handle the case where country is empty and variant present.
                # That is represented as two underscores: language__variant.
                # So if len(parts) == 2:
                #   If parts[1] is all uppercase? Actually country codes are uppercase, variant can be anything.
                #   But we cannot rely on casing because variant could be uppercase.
                # Better to follow the original logic: after split, we need to interpret based on length and content.
                # Let's adopt a more robust approach: reconstruct the original string and parse manually.
                pass

        # Actually, the original code's logic is flawed for empty country. Let's reimplement from scratch.
        # We'll parse the string manually, similar to the original but handling double underscore.
        # We can iterate through the string and find the positions of underscores.
        # But a simpler approach: use regex? Not allowed maybe.
        # Let's do manual parsing:
        # 1. Check length minimum 2.
        # 2. First two chars must be lowercase letters.
        # 3. Then we look for underscores.
        # We need to handle three formats:
        #   language
        #   language_country
        #   language_country_variant
        #   language__variant  (country empty)
        # So we need to detect if after language we have '__' (two underscores) meaning empty country.
        # We can find the first underscore after language.
        # If the next character after that underscore is also underscore, then country is empty.

        # Let's implement:
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")

        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Find first underscore
        try:
            first_underscore = locale_str.index('_')
        except ValueError:
            first_underscore = -1

        if first_underscore == -1:
            # No underscore: just language
            if length == 2:
                return Locale(locale_str, "")
            else:
                # language longer than 2 chars? Actually language can be 2 or 3 letters.
                # ISO 639 alpha-2 or alpha-3. So we should allow length 2 or 3.
                # But the original code only allowed length 2 for language-only? Wait: line 216: if length == 2.
                # That means it only accepts exactly 2 chars for language-only.
                # However, ISO 639 alpha-3 codes exist. The original Java Locale can handle 3-letter language codes.
                # The bug report is about empty country, not about 3-letter language.
                # We'll stick to the original validation for now, but note that the original code also had the same limitation.
                # Actually, the original code's condition: if length != 2 and length != 5 and length < 7.
                # That means language-only must be exactly 2 chars. So we keep that.
                if length == 2:
                    return Locale(locale_str, "")
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")

        # We have at least one underscore
        if first_underscore != 2 and first_underscore != 3:
            # Language must be 2 or 3 chars? Actually Java Locale allows 2 or 3 letter language.
            # But the original code assumed language is exactly 2 chars (since it checks indices 0 and 1).
            # We'll keep the original assumption: language is exactly 2 chars.
            # So first_underscore must be 2.
            raise ValueError(f"Invalid locale format: {locale_str}")

        language = locale_str[0:first_underscore]

        # Check if there is a second underscore immediately after the first
        if first_underscore + 1 < length and locale_str[first_underscore + 1] == '_':
            # Empty country: format language__variant
            country = ""
            # The variant starts after the double underscore
            variant_start = first_underscore + 2
            if variant_start >= length:
                # No variant after double underscore? That's invalid.
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[variant_start:]
            # Validate variant? Not needed.
            return Locale(language, country, variant)
        else:
            # Not empty country: could be language_country or language_country_variant
            # We need to check if there is another underscore later.
            # The country is exactly 2 uppercase letters? Actually country can be 2 or 3 letters (UN M.49).
            # But original code assumed 2 uppercase letters.
            # We'll follow original: country is exactly 2 uppercase letters.
            if first_underscore + 2 >= length:
                raise ValueError(f"Invalid locale format: {locale_str}")
            ch3 = locale_str[first_underscore + 1]
            ch4 = locale_str[first_underscore + 2]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = locale_str[first_underscore + 1: first_underscore + 3]

            # Check for variant
            if first_underscore + 3 < length:
                # There is more after country
                if locale_str[first_underscore + 3] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant_start = first_underscore + 4
                if variant_start >= length:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[variant_start:]
                return Locale(language, country, variant)
            else:
                # No variant
                return Locale(language, country, "")
    
    # -----------------------------------------------------------------------
    @classmethod
    def locale_lookup_list(cls, locale: Locale, default_locale: Locale = None) -> List[Locale]:
        """
        Obtains the list of locales to search through when performing
        a locale search.

        Examples:
            locale_lookup_list(Locale("fr","CA","xxx"))
              = [Locale("fr","CA","xxx"), Locale("fr","CA"), Locale("fr")]
            
            locale_lookup_list(Locale("fr", "CA", "xxx"), Locale("en"))
              = [Locale("fr","CA","xxx"), Locale("fr","CA"), Locale("fr"), Locale("en")]

        The result list begins with the most specific locale, then the
        next more general and so on, finishing with the default locale.
        The list will never contain the same locale twice.

        Args:
            locale: the locale to start from, None returns empty list
            default_locale: the default locale to use if no other is found
                           (if None, uses locale as default)
            
        Returns:
            the unmodifiable list of Locale objects, 0 being locale, never None
        """
        if default_locale is None:
            default_locale = locale
        
        result_list = []
        if locale is not None:
            result_list.append(locale)
            if len(locale.get_variant()) > 0:
                result_list.append(Locale(locale.get_language(), locale.get_country()))
            if len(locale.get_country()) > 0:
                result_list.append(Locale(locale.get_language(), ""))
            if default_locale not in result_list:
                result_list.append(default_locale)
        
        return tuple(result_list)  # Return as tuple for immutability
    
    # -----------------------------------------------------------------------
    @classmethod
    def available_locale_list(cls) -> List[Locale]:
        """
        Obtains an unmodifiable list of installed locales.

        This method is a wrapper around Locale.get_available_locales().
        It is more efficient, as the JDK method must create a new array each
        time it is called.

        Returns:
            the unmodifiable list of available locales
        """
        cls._ensure_initialized()
        return cls._c_available_locale_list
    
    # -----------------------------------------------------------------------
    @classmethod
    def available_locale_set(cls) -> FrozenSet[Locale]:
        """
        Obtains an unmodifiable set of installed locales.

        This method is a wrapper around Locale.get_available_locales().
        It is more efficient, as the JDK method must create a new array each
        time it is called.

        Returns:
            the unmodifiable set of available locales
        """
        locale_set = cls._c_available_locale_set
        if locale_set is None:
            locale_set = frozenset(cls.available_locale_list())
            cls._c_available_locale_set = locale_set
        return locale_set
    
    # -----------------------------------------------------------------------
    @classmethod
    def is_available_locale(cls, locale: Locale) -> bool:
        """
        Checks if the locale specified is in the list of available locales.

        Args:
            locale: the Locale object to check if it is available
            
        Returns:
            True if the locale is a known locale
        """
        return locale in cls.available_locale_list()
    
    # -----------------------------------------------------------------------
    @classmethod
    def languages_by_country(cls, country_code: str) -> List[Locale]:
        """
        Obtains the list of languages supported for a given country.

        This method takes a country code and searches to find the
        languages available for that country. Variant locales are removed.

        Args:
            country_code: the 2 letter country code, None returns empty
            
        Returns:
            an unmodifiable List of Locale objects, never None
        """
        with cls._languages_by_country_lock:
            langs = cls._c_languages_by_country.get(country_code)  # syncd
        
        if langs is None:
            if country_code is not None:
                langs = []
                locales = cls.available_locale_list()
                for i in range(len(locales)):
                    locale = locales[i]
                    if country_code == locale.get_country() and \
                            len(locale.get_variant()) == 0:
                        langs.append(locale)
                langs = tuple(langs)  # Unmodifiable
            else:
                langs = ()  # EMPTY_LIST equivalent
            
            with cls._languages_by_country_lock:
                cls._c_languages_by_country[country_code] = langs  # syncd
        
        return langs
    
    # -----------------------------------------------------------------------
    @classmethod
    def countries_by_language(cls, language_code: str) -> List[Locale]:
        """
        Obtains the list of countries supported for a given language.

        This method takes a language code and searches to find the
        countries available for that language. Variant locales are removed.

        Args:
            language_code: the 2 letter language code, None returns empty
            
        Returns:
            an unmodifiable List of Locale objects, never None
        """
        with cls._countries_by_language_lock:
            countries = cls._c_countries_by_language.get(language_code)  # syncd
        
        if countries is None:
            if language_code is not None:
                countries = []
                locales = cls.available_locale_list()
                for i in range(len(locales)):
                    locale = locales[i]
                    if language_code == locale.get_language() and \
                            len(locale.get_country()) != 0 and \
                            len(locale.get_variant()) == 0:
                        countries.append(locale)
                countries = tuple(countries)  # Unmodifiable
            else:
                countries = ()  # EMPTY_LIST equivalent
            
            with cls._countries_by_language_lock:
                cls._c_countries_by_language[language_code] = countries  # syncd
        
        return countries