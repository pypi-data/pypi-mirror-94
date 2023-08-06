import os
from enum import Enum

from typing import Dict, List, Union
from pronouns_test_data.models import GeneratedTestData, PronounTestCase, ValidCharacters
from pronouns_test_data.generate import generate_test_data

__all__ = [
    'DataFormat',
    'load_published_data',
    'GeneratedTestData',
    'generate_test_data',
    'PronounTestCase',
    'ValidCharacters'
]


class DataFormat(Enum):
    model = 'model'
    dict_list = 'list'
    raw_json = 'raw_json'
    raw_csv = 'raw_csv'


def load_published_data(
        version: str = 'latest',
        data_format: DataFormat = DataFormat.model
) -> Union[GeneratedTestData, List[Dict[str, str]], str]:
    """

    :param version: The version to load (e.g., 1.0.0; defaults to 'latest')
    :param data_format: How you would like the data returned:
        DataFormat.model: Returns an instance of models.GeneratedTestData
        DataFormat.list: Returns [{"uwnetid": "foo", "pronoun": "bar", "use_case": "baz"}, ...]
        DataFormat.raw_json: Returns the raw json document, for you to parse.
        DataFormat.raw_csv: Returns the raw CSV document, for you to parse.
    :return: The version of the data requested in the format requested.
    """
    here_ = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(here_, 'data')
    file_suffix = 'csv' if data_format == DataFormat.raw_csv else 'json'
    file_name = os.path.join(data_dir, f'{version}.{file_suffix}')
    with open(file_name) as f:
        raw_data = f.read()
    if data_format.value.startswith('raw'):
        return raw_data
    model = GeneratedTestData.parse_raw(raw_data)
    if data_format == DataFormat.dict_list:
        return model.dict()['test_cases']
    return model
