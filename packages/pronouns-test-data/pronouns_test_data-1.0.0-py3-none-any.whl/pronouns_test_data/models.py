import string
from typing import List

from pydantic import BaseModel, Field
from inflection import camelize


class _BaseModel(BaseModel):
    class Config:
        @staticmethod
        def camelize_(value: str) -> str:
            return camelize(value, uppercase_first_letter=False)

        allow_population_by_field_name = True
        alias_generator = camelize_


class ValidCharacters(str):
    @staticmethod
    def illegal_punctuation() -> str:
        return "|\\"

    @classmethod
    def valid_punctuation(cls) -> str:
        punctuation = string.punctuation
        for char in cls.illegal_punctuation():
            punctuation = punctuation.replace(char, "")
        return punctuation

    @classmethod
    def valid_ascii(cls):
        return string.ascii_letters + string.digits + cls.valid_punctuation() + " "


class PronounTestCase(_BaseModel):
    uwnetid: str
    pronoun: str
    use_case: str = Field(
        ..., description="A description of what this case is testing."
    )


class GeneratedTestData(BaseModel):
    test_cases: List[PronounTestCase] = []
