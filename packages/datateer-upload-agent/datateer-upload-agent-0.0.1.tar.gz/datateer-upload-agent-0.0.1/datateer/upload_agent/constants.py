SAMPLE_FEED = {
    "provider": "SAMPLE-PROVIDER",
    "source": "SAMPLE-SOURCE",
    "feed": "SAMPLE-FEED",
}

SAMPLE_CONFIG = {
    "client-code": "SAMPLE-CLIENT-CODE",
    "upload-agent": {
        "raw-bucket": "SAMPLE-RAW-BUCKET",
        "access-key": "SAMPLE-ACCESS-KEY",
        "access-secret": "SAMPLE-ACCESS-SECRET",
        "feeds": {
            "SAMPLE-FEED-1": SAMPLE_FEED
        }
    },
}

KEY_TEMPLATE = '{provider}/{source}/{feed}/export_date={export_date}/{file}'