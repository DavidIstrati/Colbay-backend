from .regexString import REGEX_STRING
import re

class StringStandardizer():
    def __init__(self, value: str):
        self.value = value

    def removeWhitespace(self):
        return StringStandardizer(re.sub(REGEX_STRING['whitespace'], " ", self.value))

    def removeSpecialCharacters(self):
        return StringStandardizer(re.sub(REGEX_STRING['lettersNumbersSpaces'], "", self.value))

    def lowercase(self):
        return StringStandardizer(self.value.lower())

    def trim(self):
        return StringStandardizer(self.value.strip())

    def getValue(self):
        return self.value