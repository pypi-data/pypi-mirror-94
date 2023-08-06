from datateer.upload_agent.upload import format_s3_key
from unittest.mock import patch

from freezegun import freeze_time
import datetime
import unittest

@patch('datateer.upload_agent.upload.get_feed')
@freeze_time('2021-02-20')
def test_format_s3_key_date_format_ccyy_mm_dd(mock_get_feed):
    # arrange
    feed_key = 'test_feed_key'
    file_name = 'test.csv'
    # act
    return_value = format_s3_key(feed_key, file_name)
    # assert
    assert '2021-02-20' in return_value
    assert '2021-20-02' not in return_value
