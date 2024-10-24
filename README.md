<div>
<img src="https://github.com/mage-ai/assets/blob/main/mascots/mascots-shorter.jpeg?raw=true">
</div>


# Mini-Project: Building an ETL Pipeline Orchestrated by Mage

This project is based on the workflow orchestration framework [Mage](https://www.mage.ai/). 

More about the framework, please see the document [here](https://docs.mage.ai/introduction/overview). 

[Get Started](https://github.com/mage-ai/mage-zoomcamp?tab=readme-ov-file#lets-get-started)
[Assistance](https://github.com/mage-ai/mage-zoomcamp?tab=readme-ov-file#assistance)

## Mage installation

This repo contains a Docker Compose template for getting started with a new Mage project. It requires Docker to be installed locally.

You can start by cloning the repo:

```bash
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp
```

Navigate to the repo:

```bash
cd mage-data-engineering-zoomcamp
```

Rename `dev.env` to simply `.env`— this will _ensure_ the file is not committed to Git by accident, since it _will_ contain credentials in the future.

Build the container

```bash
docker compose build
```

Finally, start the Docker container:

```bash
docker compose up
```

Now, navigate to http://localhost:6789 in your browser!

## Project structure

This repository should have the following structure:

```
.
├── mage_data
│   └── magic-zoomcamp
├── magic-zoomcamp
│   ├── __pycache__
│   ├── charts
│   ├── custom
│   ├── data_exporters
│   ├── data_loaders
│   ├── dbt
│   ├── extensions
│   ├── interactions
│   ├── pipelines
│   ├── scratchpads
│   ├── transformers
│   ├── utils
│   ├── __init__.py
│   ├── io_config.yaml
│   ├── metadata.yaml
│   └── requirements.txt
├── Dockerfile
├── README.md
├── dev.env
├── docker-compose.yml
└── requirements.txt
```

## GCP Credential and Storage Setup

### Create Service Account
On Google Cloud Platform, within the project you created, you need to set up a service account to allow Mage to access your GCP resources.

We add a GCP Service account with the following roles:
- Service Account Token Creator
- Cloud Run Developer
- Artifact Registry Reader
- Owner
- Artifact Registry Writer

After creating the service account, download the JSON key file and save it.

In the project, access `magic-zoomcamp/io_config.yaml` and update the `default:` profile adding the service account credentials.
```yaml
GOOGLE_SERVICE_ACC_KEY_FILEPATH: <path-to-your-service-account-key-file>
GOOGLE_LOCATION: <EU/US>
```

## PostgreSQL Setup

This option is for users who want to use a PostgreSQL to be the data warehouse for the project.
In the project, access `magic-zoomcamp/io_config.yaml` and update the `dev:` profile adding the connection variables.
```yaml
dev:
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{env_var('POSTGRES_DBNAME')}}"
  POSTGRES_SCHEMA: "{{env_var('POSTGRES_SCHEMA')}}"
  POSTGRES_USER: "{{env_var('POSTGRES_USER')}}"
  POSTGRES_PASSWORD: "{{env_var('POSTGRES_PASSWORD')}}"
  POSTGRES_HOST: "{{env_var('POSTGRES_HOST')}}"
  POSTGRES_PORT: "{{env_var('POSTGRES_PORT')}}"
```
Environment variables to define in `.env` file:
Example:
```bash
PROJECT_NAME=magic-zoomcamp
POSTGRES_DBNAME=postgres
POSTGRES_SCHEMA=magic
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

## Project:

In this section, the content is what i have learned during the discovery of this framework. 

### Structure of a ETL:

In each pipeline, there are many procedures. Each procedure has it own function. We call a piece of code which execute 1 function to be a *block*. In Mage, we can devise our workflow in to many blocks. Mage provide us 3 types of blocks for 3 functions differents: Data Loader, Data Transformer and Data Exporter.

1. Data Loader: 

Data loader reads data from a source and returns a DataFrame.

Example:
```python
import io
import pandas as pd
import requests
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    """
    Template for loading data from API
    """
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv?raw=True'

    return pd.read_csv(url)


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
assert df is not None, 'The output is undefined'
```
Explain: This data loader ( python ) load data from an API. We use the *pandas* module for loading the data under .csv format. Finally, we test if the data is not null.

2. Data Transformer:
- Data transformer takes a **DataFrame as input** and returns a **DataFrame as output**.
- Data transformer method is decorated with `@transformer`, so as data loader is decorated with `@data_loader` and test is decorated with `@test`.
- `args` and `kwargs` are used to pass data from parent blocks:
    - `args`: The output from any additional upstream blocks (if applicable).
    - `kwargs`: Additional keyword arguments.
Example:
```python
from pandas import DataFrame
import math

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def select_number_columns(df: DataFrame) -> DataFrame:
    return df[['Age', 'Fare', 'Parch', 'Pclass', 'SibSp', 'Survived']]


def fill_missing_values_with_median(df: DataFrame) -> DataFrame:
    for col in df.columns:
        values = sorted(df[col].dropna().tolist())
        median_value = values[math.floor(len(values) / 2)]
        df[[col]] = df[[col]].fillna(median_value)
    return df


@transformer
def transform_df(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        df (DataFrame): Data frame from parent block.

    Returns:
        DataFrame: Transformed data frame
    """
    # Specify your transformation logic here

    return fill_missing_values_with_median(select_number_columns(df))


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
```












