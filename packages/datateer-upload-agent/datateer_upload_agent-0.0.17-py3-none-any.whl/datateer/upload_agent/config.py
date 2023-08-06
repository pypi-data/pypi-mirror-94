from pathlib import Path

import click
import yaml

DEFAULT_PATH = '.datateer/config.yml'

def load_config(path: str=DEFAULT_PATH):
    config_file = Path(path)
    if config_file.exists():
        with open(config_file.resolve()) as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    else:
        return {}


def save_config(updated_config, path: str=DEFAULT_PATH):
    # ensure the path exists
    parent_path = Path(path).resolve().parent
    parent_path.mkdir(parents=True, exist_ok=True)

    # save the config
    with open(path, 'w') as file:
        yaml.dump(updated_config, file)

    # reload the config
    return updated_config
    

def save_feed(key, feed, path: str=DEFAULT_PATH):
    config = load_config(path)
    if 'upload-agent' not in config:
        raise click.ClickException('Could not find configuration. Run "datateer config upload-agent" before configuring any feeds"')
    if 'feeds' not in config['upload-agent']:
        config['upload-agent']['feeds'] = {}
    config['upload-agent']['feeds'][key] = feed

    save_config(config)

def get_feed(key, path: str=DEFAULT_PATH):
    config = load_config(path)
    feed = config.get('upload-agent', {}).get('feeds', {}).get(key)
    if not feed:
        raise click.ClickException(f'Feed with key {key} does not exist')
    return feed
    