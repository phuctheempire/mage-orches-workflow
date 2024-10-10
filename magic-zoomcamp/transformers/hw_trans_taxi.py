import re
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(name):
    # Replace capital letters with '_lowercase' (ignoring the first character)
    name = re.sub(r'(?<!^)(?<!^)(?=[A-Z])', '_', name).lower().replace('_i_d', '_id')
    return name


@transformer
def transform(data, *args, **kwargs):
    data = data[data['passenger_count'] > 0 ]
    data = data[data['trip_distance'] > 0]
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data.columns = [camel_to_snake(col) for col in data.columns]
    print(data)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert "vendor_id" in output.columns, 'vendor_id is not in column'
    for val in output['passenger_count']:
        assert val > 0, 'There are rows that passenger count <= 0'
    for val in output['trip_distance']:
        assert val > 0, 'There are rows that trip_distance <= 0'
