import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    taxi_dtypes = {
        'VendorID':pd.Int64Dtype(),
        'passenger_count':pd.Int64Dtype(),
        'trip_distance':float,
        'RatecodeID':float,
        'store_and_fwd_flag':str,
        'PULocationID':pd.Int64Dtype(),
        'DOLocationID':pd.Int64Dtype(),
        'payment_type':pd.Int64Dtype(),
        'fare_amount':float,
        'extra':float,
        'mta_tax':float,
        'tip_amount':float,
        'tolls_amount':float,
        'improvement_surcharge':float,
        'total_amount':float,
        'congestion_surcharge':float
    }

    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']  

    df = None
    for i in range(3):
        url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{i+10}.csv.gz"
        print(url)
        
        if i == 0 :
            
            df = pd.read_csv(url, compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
        
        else:
            load = pd.read_csv(url, compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)

            df = pd.concat([df, load], axis = 0)
    # url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-09.csv.gz'
    print(pd.io.sql.get_schema(df, name='green'))
    print(df.head())
    # df = pd.read_csv(url, compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
    return df



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
