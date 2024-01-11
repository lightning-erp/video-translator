import re
from string import ascii_uppercase


def split_acronyms(text: str) -> str:
    words = [split_acronym(word) for word in text.split()]

    return " ".join(words).strip()


def split_acronym(word: str) -> str:
    characters_or_digits = r"\d+|\D+"
    segments = re.findall(characters_or_digits, word)
    segments = [split_if_acronym(segment) for segment in segments]
    return " ".join(segments).strip()


def split_if_acronym(segment: str) -> str:
    if all([letter in ascii_uppercase for letter in segment]):
        return " ".join(list(segment)).strip()
    else:
        return segment
