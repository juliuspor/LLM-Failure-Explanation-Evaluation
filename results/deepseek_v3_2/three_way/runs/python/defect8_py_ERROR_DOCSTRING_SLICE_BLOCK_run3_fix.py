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
        """
        Parse a locale string into a `Locale` object.

        This translation follows the underscore-separated forms used by the
        Java implementation and validates casing and separators.

        Examples:
            LocaleUtils.to_locale("en")        -> Locale("en", "")
            LocaleUtils.to_locale("en_GB")     -> Locale("en", "GB")
            LocaleUtils.to_locale("en_GB_xxx") -> Locale("en", "GB", "xxx")

        Args:
            locale_str: Locale string to convert. If None, returns None.

        Returns:
            A `Locale` instance, or None if `locale_str` is None.

        Raises:
            ValueError: If `locale_str` does not match the expected format.
        """
        if locale_str is None:
            return None

        # Split by underscore, but handle consecutive underscores as empty segments
        parts = locale_str.split('_')
        # Remove empty strings that result from consecutive underscores? Actually, we need to preserve them as empty segments.
        # But the Java Locale parsing treats consecutive underscores as empty country or variant.
        # For example, "fr__POSIX" -> language="fr", country="", variant="POSIX"
        # So we need to handle the case where we have more than 3 parts due to empty segments.
        # Let's re-parse more robustly.

        # We'll iterate through the string and find the positions of underscores.
        # But simpler: we can use the original logic but adjust for empty segments.
        # The Java implementation in LocaleUtils (from Apache Commons) handles this.
        # Looking at the original Java code, it does:
        #   int len = str.length();
        #   if (len != 2 && len != 5 && len < 7) {
        #       throw new IllegalArgumentException("Invalid locale format: " + str);
        #   }
        #   ...
        # That's exactly what we have, but it fails for "fr__POSIX" because length is 9, but the check expects at least 7.
        # Actually length 9 passes the length check (>=7). Then it checks:
        #   if (str.charAt(2) != '_') ...
        #   ch3 = str.charAt(3); ch4 = str.charAt(4);
        #   if (ch3 < 'A' || ch3 > 'Z' || ch4 < 'A' || ch4 > 'Z') ...
        # For "fr__POSIX", str.charAt(2) is '_' (ok), but ch3 is '_' (not uppercase letter) -> error.
        # So we need to handle empty country code.
        # The Java Locale class itself can parse "fr__POSIX" via the constructor Locale(String language, String country, String variant).
        # But LocaleUtils.toLocale is stricter.
        # However, the bug report says the function fails for "fr__POSIX". We need to fix it to accept such format.
        # Let's implement a more flexible parsing: split by '_' and then interpret.
        # According to Java Locale, the format is: language + "_" + country + "_" + variant
        # where country and variant can be empty. So "fr__POSIX" means language=fr, country=empty, variant=POSIX.
        # Similarly, "en__POSIX" etc.
        # So we can parse by splitting on '_' and then assign parts.
        # But note: variant can contain underscores? In Java, variant is the rest after the second underscore.
        # So we need to split into at most 3 parts, but keep empty strings for missing parts.
        # We can use partition twice.

        # First, find the first underscore.
        first_underscore = locale_str.find('_')
        if first_underscore == -1:
            # No underscore: just language
            language = locale_str
            country = ''
            variant = ''
        else:
            language = locale_str[:first_underscore]
            rest = locale_str[first_underscore+1:]
            # Now find the second underscore in the rest
            second_underscore = rest.find('_')
            if second_underscore == -1:
                # Only one underscore: language_country, rest is country
                country = rest
                variant = ''
            else:
                # Two or more underscores: country is before second underscore, variant is after
                country = rest[:second_underscore]
                variant = rest[second_underscore+1:]

        # Validate language: must be two letters, lowercase? Actually ISO 639 can be 2 or 3 letters.
        # But the original code only accepted 2-letter language codes? It checked first two characters are lowercase.
        # We'll keep the validation similar but more flexible.
        if not language:
            raise ValueError(f"Invalid locale format: {locale_str}")
        for ch in language:
            if ch < 'a' or ch > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")

        # Validate country: if present, must be two uppercase letters or empty
        if country:
            if len(country) != 2:
                # Could be three-digit UN M.49? The Locale constructor allows any string for country.
                # But the original validation expected exactly two uppercase letters.
                # We'll relax to allow any uppercase letters? Actually Java Locale allows any two uppercase letters or three digits.
                # We'll follow the original stricter validation for compatibility.
                # However, for "fr__POSIX", country is empty, so we skip.
                # For other cases, we want to accept two uppercase letters.
                # Let's check: if country length is 2, both uppercase; else raise.
                raise ValueError(f"Invalid locale format: {locale_str}")
            for ch in country:
                if ch < 'A' or ch > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")

        # Variant can be any string, no validation needed.

        return Locale(language, country, variant)
    
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