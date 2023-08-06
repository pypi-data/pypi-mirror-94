# Datateer upload-agent
This is a command-line tool for uploading data into your Datateer data lake.

The upload agent pushes files into an AWS S3 bucket, where the files are picked up for ingestion and further processing

## Quick start
Ensure you have python and pip installed, then follow these steps:
1. Install with `pip install datateer-upload-agent`
1. Do one-time agent configuration with `datateer config upload-agent`
1. Do one-time feed configuration with `datateer config feed`
1. Upload data with `datateer upload <feed_key> <path>`
## Concepts
All data in the data lake has the following metadata:
- A **provider** is an organization that is providing data. This could be your organization if you are pushing data from an internal database or application
- A **source** is the system or application that is providing data. A provider can provide data from one or more systems
- A **feed** is an independent data feed. A source can provide one or more feeds. For example, if the source is a database, each feed could represent a single table or view. If the source is an API, each feed could represent a single entity. 
- A **file** is a data file like a CSV file. It is a point-in-time extraction of a feed, and it is what you upload using the agent.

## Commands
### Uploading
#### Upload a file
`datateer upload orders_feed ./my_exported_data/orders.csv` will upload the file at `./my_exported_data/orders.csv` using the feed key `orders_feed`

### Configuring
#### Configure the upload agent
`datateer config upload-agent` will ask you a series of questions to configure your agent
```yaml
Datateer client code:
Raw bucket name:
Access key:
Access secret:
```

If you need to reconfigure the agent, just rerun `datateer config upload-agent`

#### Configure a new feed
`datateer config feed` will ask a series of questions to configure a new feed
```yaml
Provider: xyz
Data Source: internal_app1
Feed: orders
Feed key [orders]: orders_feed
```

#### Reconfigure an existing feed
`datateer config feed --update orders_feed` will rerun the configuration questions for the feed with the key `orders_feed`

#### Show config
`datateer config upload-agent --show` will show you your existing configuration
```yaml
client-code: xyz
raw-bucket: xyz-pipeline-raw-202012331213123432341213
access-key: ABC***
access-secret: 123***
feeds: 3
```

`datateer config feed --show` will show vlaues for all feeds you have configured
```yaml
1) Feed "customers" will upload to xyz/internal_app1/customers/
2) Feed "orders_feed" will upload to xyz/internal_app1/orders/
3) Feed "leads" will upload to salesforce/salesforce/leads
```

`datateer config feed abc --show` will show values for a feed with the key `abc`
```yaml
Feed "abc" will upload to provider/source/feed
```

## Data File Requirements
- The data lake can ingest CSV files only
- The first row of the data file must contain header names
- Adding new data fields or removing  data fields are both supported
- You should strive to be consistent with your header names over time. The data lake can handle changes, but it will likely confuse anyone using the feeds
## Configuration - detailed info
Configuration can be handled completely through the `datateer config` commands. If you need more details, this section provides more details on how configuration works and where it is stored. 

### Location
Here is where the Datateer upload agent will look for configuration information, in order of preference:
1. In a relative directory named `.datateer`, in a file named `config.yml`. 
1. In the future, we may add global configuration in the user's home directory or in environment variables

### Schema
An example configuration file will look like this:
```yaml
client-code: xyz
upload-agent: 
  raw-bucket: xyz-pipeline-raw-202012331213123432341213
  access-key: ABC***
  access-secret: 123***
  feeds:
    customers:
      provider: xyz
      source: internal_app1
      feed: customers
    orders_feed:
      provider: xyz
      source: internal_app1
      feed: orders
    leads:
      provider: salesforce
      source: salesforce
      feed: leads
```