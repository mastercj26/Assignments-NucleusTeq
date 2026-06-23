

import re
from typing import Optional

EMAIL_PATTERN: str = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
MOBILE_PATTERN: str = r"^[6-9]\d{9}$"
CAPITALIZED_WORD_PATTERN: str = r"\b[A-Z][a-z]*\b"
ALPHABET_ONLY_PATTERN: str = r"^[a-zA-Z]+$"
MULTIPLE_SPACES_PATTERN: str = r" +"
NUMBER_EXTRACTION_PATTERN: str = r"\d+"
PASSWORD_PATTERN: str = r"^(?=.*[0-9])(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]).{8,}$"


def extract_numbers_from_string(input_string: str) -> list[str]:

    extracted_numbers: list[str] = re.findall(NUMBER_EXTRACTION_PATTERN, input_string)
    return extracted_numbers


def validate_email_address(email_address: str) -> bool:

    match_result = re.match(EMAIL_PATTERN, email_address)
    return match_result is not None


def validate_mobile_number(mobile_number: str) -> bool:

    match_result = re.match(MOBILE_PATTERN, mobile_number)
    return match_result is not None


def search_word_in_sentence(word: str, sentence: str) -> bool:
    """
    Use re.search() to check whether word exists in sentence.
    """
    search_pattern: str = rf"\b{re.escape(word)}\b"
    search_result = re.search(search_pattern, sentence)
    return search_result is not None


def extract_capitalized_words(input_string: str) -> list[str]:
    """
    Use re.findall() to extract all words starting with a capital letter.
    """
    capitalized_words: list[str] = re.findall(CAPITALIZED_WORD_PATTERN, input_string)
    return capitalized_words


def normalize_whitespace(input_string: str) -> str:

    normalized_string: str = re.sub(MULTIPLE_SPACES_PATTERN, " ", input_string)
    return normalized_string.strip()


def contains_only_alphabets(input_string: str) -> bool:
    """
    Check whether input_string contains only alphabetic characters.
    """
    match_result = re.match(ALPHABET_ONLY_PATTERN, input_string)
    return match_result is not None


def validate_password_strength(password: str) -> bool:

    match_result = re.match(PASSWORD_PATTERN, password)
    return match_result is not None