import json
import importlib
import random
import string
from uuid import uuid4
from importlib import reload
from configtor import render


def random_string(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def test_config():
    fake_common = {}
    for _ in range(5):
        fake_common[random_string()] = random_string()

    stg_data = {}
    for key, _ in fake_common.items():
        stg_data[key] = random_string()

    fake_data = {
        "templates": [
            {
                "path": "./tests/templates",
                "name": "template.py",
                "dest": "./tests/test_result.py"
            }
        ],
        "common": fake_common,
        "stg": stg_data
    }

    fake_temp_str = '\n'.join(
        [f"{key} = '{{{{ {key} }}}}'" for key, value in fake_common.items()])

    expected_str = '\n'.join(
        [f"{key} = '{value}'" for key, value in fake_common.items()])

    stg_str = '\n'.join(
        [f"{key} = '{value}'" for key, value in stg_data.items()])

    with open('./tests/data.json', 'w') as data_file:
        json.dump(fake_data,
                  data_file,
                  indent=4)

    with open('./tests/templates/template.py', 'w') as temp_file:
        temp_file.write(fake_temp_str)

    render('./tests/data.json')
    with open('./tests/test_result.py', 'r') as result_file:
        assert expected_str == result_file.read()

    render('./tests/data.json', stage='stg')
    with open('./tests/test_result.py', 'r') as result_file:
        assert stg_str == result_file.read()
