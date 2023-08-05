import os
from pathlib import Path

import pytest

from datateer.upload_agent import config
from datateer.upload_agent.config import load_config, save_config, save_feed
import datateer.upload_agent.constants as constants

TEST_FILES_DIR = Path(__file__).resolve().parent / 'files'

def test_load_config():
    path = TEST_FILES_DIR / 'config_file1.yml'
    config = load_config(path)
    assert config['client-code'] == 'xyz'
    assert config['upload-agent']['raw-bucket'] == 'xyz-pipeline-raw-202012331213123432341213'
    assert config['upload-agent']['access-key'] == 'ABCABC'
    assert config['upload-agent']['access-secret'] == '123123'
    assert config['upload-agent']['feeds']['customers']['provider'] == 'xyz'
    assert config['upload-agent']['feeds']['customers']['source'] == 'internal_app1'
    assert config['upload-agent']['feeds']['customers']['feed'] == 'customers'
    assert config['upload-agent']['feeds']['orders_feed']['provider'] == 'xyz'
    assert config['upload-agent']['feeds']['orders_feed']['source'] == 'internal_app1'
    assert config['upload-agent']['feeds']['orders_feed']['feed'] == 'orders'
    assert config['upload-agent']['feeds']['leads']['provider'] == 'salesforce'
    assert config['upload-agent']['feeds']['leads']['source'] == 'salesforce'
    assert config['upload-agent']['feeds']['leads']['feed'] == 'leads'

def test_save_config_creates_config(tmp_path):
    expected = 'TEST-CLIENT-CODE'
    assert load_config().get('client-code') != expected

    new_config = {
        'client-code': expected
    }
    os.chdir(tmp_path)

    updated_config = save_config(new_config)

    assert Path(Path(tmp_path) / '.datateer/config.yml').exists()
    assert updated_config.get('client-code') == expected



def test_save_feed_creates_feed_in_config(config, config_path):
    assert 'feeds' not in config
    feed = {
        'provider': 'SAMPLE-PROVIDER',
        'source': 'SAMPLE-SOURCE',
        'feed': 'SAMPLE-FEED',
    }

    save_feed('sample-feed', feed)
    config = load_config()

    assert 'feeds' in config['upload-agent']
    assert 'sample-feed' in config['upload-agent']['feeds']
    assert config['upload-agent']['feeds']['sample-feed']['provider'] == 'SAMPLE-PROVIDER'


    
    

  

