'''configuration tool base on jinja2'''

from typing import Optional
import os
import json
import typer
from jinja2 import Environment, FileSystemLoader

__version__ = '0.0.1'

main = typer.Typer()


def write_to_file(template, data, dest):
    result = template.render(**data)
    with open(dest, 'w') as dest_file:
        dest_file.write(result)


@main.command()
def render(path: str = './scripts/data.json',
           stage: Optional[str] = None) -> None:

    with open(path) as json_file:
        json_data = json.load(json_file)

    input_data = json_data['common']
    if stage is not None:
        input_data = {**input_data, **json_data['stage']}

    for temp_data in json_data['templates']:
        file_loader = FileSystemLoader(temp_data['path'])
        env = Environment(loader=file_loader)
        template = env.get_template(temp_data['name'])
        write_to_file(template, input_data, temp_data['dest'])


@main.command()
def init(to='./scripts', templates_path='./scripts/templates'):
    try:
        os.mkdir(to)
    except OSError as exc:
        typer.echo(f'{to} is existed ,skip mkdir {to}')

    init_template = {
        'templates': [],
        'common': {},
        'dev': {},
        'stg': {},
        'prod': {}
    }
    with open(f'{to}/data.json', 'w') as data_file:
        json.dump(init_template, data_file, indent=4)

    try:
        os.mkdir(templates_path)
    except OSError as exc:
        typer.echo(f'{templates_path} is existed ,skip mkdir {templates_path}')

    typer.echo('data.json initiate success')


if __name__ == '__main__':
    main()
