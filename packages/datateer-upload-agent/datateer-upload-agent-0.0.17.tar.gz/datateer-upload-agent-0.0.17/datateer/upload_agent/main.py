import json 

import click

# import datateer.upload_agent.config as config
from .config import load_config, get_feed, save_config, save_feed, DEFAULT_PATH as default_config_path
from .upload import upload as upload_file

config = load_config()

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    

@cli.command()
# @click.argument("name")
def upload():
    pass


@cli.group(name='config')
@click.pass_context
def config_group(ctx):
    ctx.obj['config'] = load_config()


def show_upload_agent_config(ctx, param, value):
    if value:
        config = load_config()
        print(json.dumps(config, indent=4))
        ctx.exit()

@config_group.command()
@click.option('-s', '--show', is_flag=True, is_eager=True, callback=show_upload_agent_config, expose_value=False, default=False, help="Shows the configuration instead of updating it")
@click.option('-c', '--client-code', prompt=True, default=lambda: config.get('client-code'), help="Your three-character code from Datateer")
@click.option('-b', '--raw-bucket', prompt='Raw bucket name', default=lambda: config.get('upload-agent', {}).get('raw-bucket'), help='The name of your data lake\'s raw bucket')
@click.option('-k', '--access-key', prompt=True, default=lambda: config.get('upload-agent', {}).get('access-key'), help='The AWS access key of your upload agent')
@click.option('-a', '--access-secret', prompt=True, default=lambda: config.get('upload-agent', {}).get('access-secret'), help='The AWS secret key of your upload agent')
def upload_agent(access_key, access_secret, client_code, raw_bucket):
    config = load_config()
    config['client-code'] = client_code
    config['upload-agent'] = {
        'raw-bucket': raw_bucket,
        'access-key': access_key,
        'access-secret': access_secret
    }
    config = save_config(config)
    click.echo(f'Saved configuration to {default_config_path}')


def show_feed_config(ctx, param, value):
    if value:
        config = load_config()
        feed = get_feed(value)
        if not feed:
            raise click.ClickException(f'Feed with key {value} does not exist')
        print(json.dumps(feed, indent=4))
        ctx.exit()


feed_to_update = None
feed_key = None
def cache_feed_key(ctx, param, value):
    if value:
        # ctx.obj['feed-key'] = value
        global feed_to_update
        global feed_key
        feed_key = value
        config = load_config()
        feed_to_update = config.get('upload-agent', {}).get('feeds', {}).get(value, {})
        if not feed_to_update:
            raise click.ClickException(f'Feed with key {value} does not exist')
        return value

def get_feed_attribute_default(param):
    global feed_to_update
    global feed_key
    if not feed_to_update:
        if param == 'provider':
            config = load_config()
            return config.get('client-code')
        return None

    if param == 'provider':
        return feed_to_update.get('provider')
    if param == 'source':
        return feed_to_update.get('source')
    if param == 'feed':
        return feed_to_update.get('feed')

@config_group.command()
@click.option('-u', '--update', 'feed_key', is_eager=True, default=None, callback=cache_feed_key, help='Update the feed that has this key value')
@click.option('-s', '--show', is_eager=True, callback=show_feed_config, expose_value=False, default=False, help="Shows the configuration for the feed that has this key value")
@click.option('-p', '--provider', prompt=True, default=lambda: get_feed_attribute_default('provider'), help="A provider is an organization that provides a data feed. If this is an internal data feed, leave blank to use your client code")
@click.option('-d', '--source', prompt=True, default=lambda: get_feed_attribute_default('source'), help="A provider can own one or more systems or applications that are a source of data")
@click.option('-f', '--feed', prompt=True, default=lambda: get_feed_attribute_default('feed'), help='A data source can provide one or more feeds')
def feed(feed, feed_key, provider, source):
    if feed_key is None:
        feed_key = click.prompt('Feed key', default=feed, show_default=True)

    feed = {
        'provider': provider,
        'source': source,
        'feed': feed
    }
    save_feed(feed_key, feed)



@cli.command()
@click.argument('feed-key')
@click.argument('path')
def upload(feed_key, path):
    upload_file(feed_key, path)


