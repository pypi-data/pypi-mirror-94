from __future__ import annotations

import csv
import os
import random
import string
from enum import Enum
from typing import NoReturn

import typer

from pronouns_test_data.models import (
    GeneratedTestData,
    PronounTestCase,
    ValidCharacters,
)

__all__ = [
    'generate_test_data'
]


def generate_jargon(valid_chars: str, length: int) -> str:
    return "".join([random.choice(valid_chars) for _ in range(length)])


def write_raw_data(filename: str, data: str) -> NoReturn:
    with open(filename, 'w') as f:
        f.write(data)
    typer.echo(f"Wrote JSON data to {filename}")


def write_csv_data(filename: str, data: GeneratedTestData):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(PronounTestCase.__fields__.keys()))
        writer.writeheader()
        for case in data.test_cases:
            writer.writerow(case.dict())
    typer.echo(f"Wrote CSV data to {filename}")


def generate_test_data() -> GeneratedTestData:
    return GeneratedTestData(
        test_cases=[
            PronounTestCase(
                uwnetid="javerage",
                pronoun="they/them/their/theirs/themself",
                use_case="The full expression of a single pronoun set. "
                "Also, this netid should be registered for some university classes.",
            ),
            PronounTestCase(
                uwnetid="uwitpn01",
                pronoun="she/her/hers; they/them/theirs",
                use_case="A consistently formatted list of two pronoun sets.",
            ),
            PronounTestCase(
                uwnetid="uwitpn02",
                pronoun="he him his",
                use_case="A single, atypically formatted pronoun set.",
            ),
            PronounTestCase(
                uwnetid="uwitpn03",
                pronoun="she, her, hers or they/them",
                use_case="Two atypically and inconsistently formatted pronoun sets.",
            ),
            PronounTestCase(
                uwnetid="uwitpn04",
                pronoun="please use my name",
                use_case="Guidance in place of a declared pronoun set, with no punctuation.",
            ),
            PronounTestCase(
                uwnetid="uwitpn05",
                pronoun="i am exploring this. please ask me!",
                use_case="Guidance in place of a declared pronoun set, with punctuation.",
            ),
            PronounTestCase(
                uwnetid="uwitpn06",
                pronoun="they/them/theirs;they/them/theirs;they/them/theirs",
                use_case="A consistently formatted pronoun set that is (accidentally?) pasted three times, with no spaces.",
            ),
            PronounTestCase(
                uwnetid="uwitpn07",
                pronoun="she/they",
                use_case="A common shorthand expression of two pronoun sets.",
            ),
            PronounTestCase(
                uwnetid="uwitpn08",
                pronoun="ze/hir",
                use_case="A common shorthand expression of two neo-pronoun sets.",
            ),
            PronounTestCase(
                uwnetid="uwitpn09",
                pronoun="fae/r or they/themself",
                use_case='One neo-pronoun shorthand and one shorthand expression of the "they" pronoun set, each with its '
                "own shorthand syntax",
            ),
            PronounTestCase(
                uwnetid="uwitpn10",
                pronoun='""el"&maybe "els" or just ask?',
                use_case="A pronoun, plus guidance, with inconsistent punctuation.",
            ),
            PronounTestCase(
                uwnetid="uwitpn11",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 12),
                use_case="12 randomly generated characters (very common length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn12",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 16),
                use_case="16 randomly generated characters (very common length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn13",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 32),
                use_case="32 randomly generated characters (uncommon length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn14",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 64),
                use_case="64 randomly generated characters (unlikely length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn15",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 128),
                use_case="128 randomly generated characters (very unlikely length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn16",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 140),
                use_case="140 (max. length) randomly generated characters (very unlikely length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn17",
                pronoun=generate_jargon(ValidCharacters.valid_punctuation(), 140),
                use_case="140 characters of only punctuation, to test text wrapping",
            ),
            PronounTestCase(
                uwnetid="uwitpn18",
                pronoun=generate_jargon(string.digits, 140),
                use_case="140 characters of only punctuation, to test text wrapping",
            ),
        ]
    )


class OutputType(Enum):
    json = 'json'
    csv = 'csv'


def app(
    out: str = typer.Option(
        "data",
        "--output-path",
        "-o",
        help="The directory "
    ),
    file_prefix: str = typer.Option(
        "iam-pronouns-test-data",
        "--file-prefix",
        "-f",
        help="The filename to use before the filetype extension (e.g., the `foo` in `foo.json`)"
    )
):
    test_data = generate_test_data()
    if not os.path.exists(out):
        os.makedirs(out, exist_ok=True)

    json_out = os.path.join(out, f'{file_prefix}.json')
    csv_out = os.path.join(out, f'{file_prefix}.csv')

    test_json = test_data.json(by_alias=True, indent=4)
    write_raw_data(json_out, test_json)
    write_csv_data(csv_out, test_data)


if __name__ == "__main__":
    typer.run(app)
