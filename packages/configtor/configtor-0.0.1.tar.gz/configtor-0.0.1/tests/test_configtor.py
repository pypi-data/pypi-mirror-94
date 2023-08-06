import json
import random
import string
from uuid import uuid4
from importlib import reload
from configtor import main


def random_string(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def test_config():
    fake_common = {}
    for _ in range(5):
        fake_common[random_string()] = random_string()

    fake_data = {
        "templates": [
            {
                "path": "./tests/templates",
                "name": "template.py",
                "dest": "./tests/test_result.py"
            }
        ],
        "common": fake_common
    }

    fake_temp_str = '\n'.join(
        [f"{key} = '{{{{ {key} }}}}'" for key, value in fake_common.items()])

    with open('./tests/data.json', 'w') as data_file:
        json.dump(fake_data,
                  data_file,
                  indent=4)

    with open('./tests/templates/template.py', 'w') as temp_file:
        temp_file.write(fake_temp_str)

    from tests import test_result
    main('./tests/data.json')
    reload(test_result)

    for key, value in fake_common.items():
        assert getattr(test_result, key) == value
