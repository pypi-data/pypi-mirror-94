import os 
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
import pytest

from datateer.upload_agent.main import cli
from datateer.upload_agent.config import load_config, save_config, save_feed
import datateer.upload_agent.constants as constants


@pytest.fixture
def runner():
    return CliRunner()


def test_command_config_upload_agent_handles_show_option(runner):
    result = runner.invoke(cli, ['config', 'upload-agent', '--show'])
    assert result.exit_code == 0


@patch('datateer.upload_agent.main.load_config')
def test_command_config_feed_handles_show_option(mock_load_config, config, runner):
    mock_load_config.return_value = config
    result = runner.invoke(cli, ['config', 'feed', '--show', 'SAMPLE-FEED-1'])

    print(result.output)
    assert result.exit_code == 0


@patch('datateer.upload_agent.main.load_config')
def test_command_config_feed_show_option_errors_if_not_exist(mock_load_config, config, runner):
    mock_load_config.return_value = config
    result = runner.invoke(cli, ['config', 'feed', '--show', 'NONEXISTENT-KEY'])

    print(result.output)
    assert result.exit_code == 1
    assert 'Feed with key NONEXISTENT-KEY does not exist' in result.output


def test_command_upload_handles_feed_key_and_path_arguments(runner):
    result = runner.invoke(cli, ['upload', 'FEED-KEY', 'PATH'])

    print(result.output)
    assert result.exit_code == 1
    assert 'Feed with key FEED-KEY does not exist'




@patch.dict('datateer.upload_agent.main.config', constants.SAMPLE_CONFIG, clear=True)
def test_config_upload_agent_prompts_show_defaults_if_config_exists(runner, config):
    defaults = config

    result = runner.invoke(cli, ['config', 'upload-agent'], input='CLIENT-CODE\nRAW-BUCKET\nACCESS-KEY\nACCESS-SECRET')
    
    print(result.output)
    assert result.exit_code == 0
    assert f'Client code [{defaults["client-code"]}]: CLIENT-CODE' in result.output
    assert f'Raw bucket name [{defaults["upload-agent"]["raw-bucket"]}]: RAW-BUCKET' in result.output
    assert f'Access key [{defaults["upload-agent"]["access-key"]}]: ACCESS-KEY' in result.output
    assert f'Access secret [{defaults["upload-agent"]["access-secret"]}]: ACCESS-SECRET' in result.output

@patch.dict('datateer.upload_agent.main.config', {'client-code': 'TEST-CLIENT-CODE'}, clear=True)
@patch('datateer.upload_agent.main.load_config')
def test_config_feed_prompts(mock_load_config, runner, config):
    mock_load_config.return_value = config
    result = runner.invoke(cli, ['config', 'feed'], input='PROVIDER\nSOURCE\nFEED\nFEED-KEY')

    print(config)
    print(result.output)
    assert result.exit_code == 0
    assert 'Provider [SAMPLE-CLIENT-CODE]: PROVIDER' in result.output
    assert 'Source: SOURCE' in result.output
    assert 'Feed: FEED' in result.output
    assert 'Feed key [FEED]: FEED-KEY' in result.output


@patch.dict('datateer.upload_agent.main.config', {'client-code': 'MY-TEST-CLIENT-CODE'})
@patch('datateer.upload_agent.main.load_config')
def test_config_feed_provider_code_defaults_to_client_code(mock_load_config, config, runner):
    mock_load_config.return_value = config
    result = runner.invoke(cli, ['config', 'feed', '--source', 'SOURCE', '--feed', 'FEED'], input='\n\n')
    assert f'Provider [{config["client-code"]}]:' in result.output
    assert f'Provider [{config["client-code"]}]: {config["client-code"]}' not in result.output # assert user did not type in a value

def test_config_feed_key_defaults_to_feed_code(runner):
    result = runner.invoke(cli, ['config', 'feed', '--provider', 'PROVIDER', '--source', 'SOURCE', '--feed', 'FEED'])
    assert 'Feed key [FEED]:' in result.output
    assert 'Feed key [FEED]: FEED' not in result.output # user did not type in a value


@patch.dict('datateer.upload_agent.main.config', constants.SAMPLE_CONFIG, clear=True)
@patch('datateer.upload_agent.main.load_config')
def test_config_feed_handles_existing_feed_key(mock_load_config, runner, config):
    mock_load_config.return_value = config
    print(config)
    result = runner.invoke(cli, ['config', 'feed', '--update', 'SAMPLE-FEED-1'], input='test\ntest\ntest\ntest\n')
    print(result.output)

    assert result.exit_code == 0
    assert f'Provider [{constants.SAMPLE_FEED["provider"]}]:' in result.output
    assert f'Source [{constants.SAMPLE_FEED["source"]}]:' in result.output
    assert f'Feed [{constants.SAMPLE_FEED["feed"]}]:' in result.output
def test_show_version(runner):
    pytest.skip()

