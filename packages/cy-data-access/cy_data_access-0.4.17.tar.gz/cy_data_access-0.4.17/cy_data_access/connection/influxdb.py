from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS


def influx_client_query_data_frame(host='http://localhost:8086', query=''):
    client = InfluxDBClient(url=host, token="", org="", debug=False)
    result = client.query_api().query_data_frame(org="", query=query)
    return result


def influx_client_query_data_frame(host='http://localhost:8086', query=''):
    """ 查询数据 """
    client = InfluxDBClient(url=host, token="", org="", debug=False)
    result = client.query_api().query_data_frame(org="", query=query)
    return result


def influx_client_write_data_frame(host='http://localhost:8086', df=None, df_time_index_name='', database='', measurement_name='', tag_columns=[]):
    """ 保存数据 """
    client = InfluxDBClient(url="http://localhost:8086", token="", org="", debug=True)
    write_client = client.write_api(write_options=WriteOptions(batch_size=500,
                                                               flush_interval=10_000,
                                                               jitter_interval=2_000,
                                                               retry_interval=5_000,
                                                               max_retries=5,
                                                               max_retry_delay=30_000,
                                                               exponential_base=2))
    df.set_index(df_time_index_name, inplace=True)
    write_client.write(database, record=df, data_frame_measurement_name=measurement_name, data_frame_tag_columns=tag_columns)
