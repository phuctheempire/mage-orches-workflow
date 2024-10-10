
### Structure of a Mage ETL

1. Data loader: 
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
    - Data loader reads data from a source and returns a DataFrame.
2. Data transformer:
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
    - Data transformer takes a DataFrame as input and returns a DataFrame as output.
    - Data transformer method is decorated with @transformer, so as data loader is decorated with @data_loader and test is decorated with @test.
    - args and kwargs are used to pass data from parent blocks:
        - args: The output from any additional upstream blocks (if applicable).
        - kwargs: Additional keyword arguments.
    - The principle is returning the transformed DataFrame.
3. Data exporter:
    Example:
    ```python
    from mage_ai.io.file import FileIO
    from pandas import DataFrame

    if 'data_exporter' not in globals():
        from mage_ai.data_preparation.decorators import data_exporter


    @data_exporter
    def export_data_to_file(df: DataFrame, **kwargs) -> None:
        """
        Template for exporting data to filesystem.

        Docs: https://docs.mage.ai/design/data-loading#example-loading-data-from-a-file
        """
        filepath = 'titanic_clean.csv'
        FileIO().export(df, filepath)
    ```
    - Data exporter takes the dataframe ( from the transformer ) and exports it to a file.
    - The data exporter method is decorated with @data_exporter.
    - The principle is the method to export and it should not return anything.
    
### Configuring GCP
1. In the project, we need to:
    - Add a service account, choose the role, and download the JSON key.
        !!! Attention: The JSON key is sensitive information. Do not share it with anyone.
    - Download the JSON key and save it in the project.
    - Enable the BigQuery API.
2. In mage, we need to configure the key:
    - In the file io_config.yaml, add the following to the default profile:
        ```yaml
        gcp:
            GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/<file_name>.json" # this is the path to the JSON key
            GOOGLE_LOCATION: EU # Optional
        ```
Now we can use the GCP service account to access the BigQuery API.
We can test it by running a data loader:
Example: A data loader -> Python -> GCS: 
We need to edit as well the bucket_name ( define the bucket name in the GCP console) and the object_key (the name of the file in the bucket).
Example:
```python
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'data_zoomcamp_xpham'
    object_key = 'titanic_clean.csv'

    return GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
```

### ETL From API to GCS:
1. Create a new pipeline ( Batch )
2. Add some interactions:
    - Extract from API ( Data Loader ):
        Example: Here, we used the existed data loader ( we use ny_taxi )
    - Transform:
        Example: We used the existed transformer ( we use ny_taxi ), we removed rows with 0 passengers
    - Load to GCS: 
        In the export: Create a new python data exporter, we define: bucket_name, object_key.
3. Option: We devide the data set into smaller chunks ( partitional uploading )
    For this, we use the module pyarrow and the function write_to_parquet.
    Some points to note:
    - We need to install the module pyarrow.
    - Credentials: We need to set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of the JSON key.
    - bucket_name: The name of the bucket in GCP.
    - project_id: The project ID in GCP.
    - table_name: The name of the table in the bucket.
    - root_path: The path to the table in the bucket.
    - Partition logic:
        - Devide the data set into smaller chunks. ( using pyarrow module, we can add partition logic )
        - We need to convert the data set into a PyArrow Table. ( using the function Table.from_pandas ). from_pandas is a method of the Table class which converts a pandas DataFrame into a PyArrow Table.
        - We need to create an instance of the GcsFileSystem class from the PyArrow library. This class allows interaction with Google Cloud Storage.
        - We need to write the PyArrow Table to a Parquet dataset in Google Cloud Storage, partitioned by the column tpep_pickup_date.

    ```python
    import pyarrow as pa
    import pyarrow.parquet as pq
    import os

    if 'data_exporter' not in globals():
        from mage_ai.data_preparation.decorators import data_exporter


    os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/src/terraform-tutorial-435313-539f83756233.json" # Tell the system where the JSON key is

    bucket_name = 'data_zoomcamp_xpham'
    project_id = 'terraform-tutorial-435313'

    table_name= "nyc_taxi_data"
    root_path = f"{bucket_name}/{table_name}"


    @data_exporter
    def export_data(data, *args, **kwargs):
        """
        Exports data to some source.

        Args:
            data: The output from the upstream parent block
            args: The output from any additional upstream blocks (if applicable)

        Output (optional):
            Optionally return any object and it'll be logged and
            displayed when inspecting the block run.
        """
        data['tpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date  
        # data['tpep_pickup_datetime'] is a Series of datetime values.
        #.dt accesses the datetime properties.
        #.date extracts the date part from each datetime value.
        
        table = pa.Table.from_pandas(data)
        #This line converts a pandas DataFrame data into a PyArrow Table

        gcs = pa.fs.GcsFileSystem()
        #This line creates an instance of the GcsFileSystem class from the PyArrow library, which allows interaction with Google Cloud Storage.

        pq.write_to_dataset(
            table,
            root_path = root_path,
            partition_cols = ['tpep_pickup_date'],
            filesystem=gcs
        )
        # This code writes a PyArrow Table table to a Parquet dataset in Google Cloud Storage, partitioned by the column tpep_pickup_date.
        # Specify your data exporting logic here

    ```

4. While running the pipeline, we can also assign parallel exporter after the transformer.

### GCS to Bigquery:
1. Create a BigQuery database ( Ex: ny_taxi )
2. Setup pipeline:
    1. Create a data loader:
        Spec: Python - GCS
        We specify the config_profile, bucket_name and object_key
    2. Create a data transformaer:
        Spec: Python - Generic
    3. Data exporter:
        Spec: SQL 
            - BigQuery
            - Schema name: ny_taxi
            - Table name: yellow_taxi_data
        Ex:
        ```sql
        SELECT * FROM {{ df_1 }};

        ```
### Setup trigger


### Paremeterised execution
- We focus on runtime variable
- We can probably use pyArrow

We note that in each block, there always be the parameter *args and **kwargs:
Those are the place storing the parameters in the pipeline:
* Need to get to know more about the arguments 
https://docs.mage.ai/development/variables/block-variables

We can add block variables by using block settings

In code
You can also create or edit block variables by going to a pipeline’s metadata.yaml file (located in the pipelines/[pipeline_uuid] directory) and adding them to a block’s configuration property.

```
blocks:
- all_upstream_blocks_executed: true
  color: null
  configuration:
    demo_block_var: block_var_value
    block_var2: val2
    block_var3: val3
  downstream_blocks: []
  executor_config: null
  executor_type: local_python
  has_callback: false
  language: python
  name: billowing snow
  retry_config: {}
  status: updated
  timeout: '60'
  type: data_exporter
  upstream_blocks:
  - muddy_waterfall
  uuid: billowing_snow
```


Access to a parameter: Using .get('variable name')
Ex: execution_date

### Backfilling 

You got missing data - you want to rerun pipelines
-> You need too construct backfill script

When you have created backfilling data -> The execution date will be base on the date on the script ( Extremely helpful for parameterized execution )
-> Data-recovery 
