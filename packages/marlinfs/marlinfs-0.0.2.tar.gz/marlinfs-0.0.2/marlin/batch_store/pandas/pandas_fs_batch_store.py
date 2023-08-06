import math
from enum import Enum
from functools import wraps

import fsspec
import uuid

from marlin.batch_store.batch_store import TransformBatchReader, BatchStore, TransformBatchWriter
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq
from marlin.batch_store.pandas.point_in_time_joiner import point_in_time_join_helper, add_uuid
from marlin.batch_store.pandas.utils import read_files_to_pandas, drop_duplicates, df_to_internal, event_time_str
from marlin.batch_store.pandas.utils import ingest_time_str
from marlin.batch_store.pandas.point_in_time_joiner import target_timestamp_str
from marlin.batch_store.pandas.point_in_time_joiner import target_timestamp_str_internal_millis

default_date_format = '%Y-%m-%d-%H'
partition_format = default_date_format
date_format_constant = 'date_format'
str_date_format_type_constant = 'str_date_format_type'


class IngestionDateFormat(Enum):
    str_date = 1
    seconds = 2


def to_millis(str_date, date_format):
    return datetime.strptime(str_date, date_format).timestamp() * 1000


def get_date_format(storage_options):
    if storage_options is None or storage_options.get(date_format_constant) is None:
        return {date_format_constant: IngestionDateFormat.str_date,
                str_date_format_type_constant: default_date_format}
    if storage_options.get(date_format_constant) == IngestionDateFormat.str_date.name:
        return {date_format_constant: IngestionDateFormat.str_date, str_date_format_type_constant:
            storage_options.get(str_date_format_type_constant, default_date_format)}
    elif storage_options.get(date_format_constant) == IngestionDateFormat.seconds.name:
        return {date_format_constant: IngestionDateFormat.seconds}
    raise Exception('Unsupported date format supplied')


class PandasS3BatchStore(BatchStore):
    def __init__(self, metadata_sore):
        super().__init__(metadata_sore)

    def batch_transform_reader(self, namespace, name, version, features):
        return PandasFSBatchReader(namespace, name, version, features, self.metadata_store)

    def batch_transform_writer(self, namespace, name, version, code, entities, input_definition):
        return PandasFSBatchWriter(self.metadata_store, namespace, name, version, code, entities, input_definition)


def str_formatted_date(x):
    return x.apply(lambda xy: xy if math.isnan(xy) else datetime.fromtimestamp(xy / 1000).strftime(partition_format))


def to_string_date(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        df = function(*args, **kwargs)
        columns = [event_time_str, ingest_time_str]
        df[columns] = df[columns].apply(str_formatted_date)
        return df

    return decorator


def add_millis_columns_from_date(entity_df, date_format):
    new_df = entity_df.copy(deep=False)
    new_df[target_timestamp_str_internal_millis] = new_df[target_timestamp_str].apply(lambda x:
                                                                                      to_millis(x, date_format))
    return new_df


def add_millis_columns_from_seconds(entity_df):
    new_df = entity_df.copy(deep=False)
    new_df[target_timestamp_str_internal_millis] = entity_df[target_timestamp_str] * 1000
    return new_df


def timestamp_handler(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        df = function(*args, **kwargs)
        df[[event_time_str, ingest_time_str]] /= 1000
        return df

    return decorator


def internal_point_in_time_join_return_handler(df):
    return drop_duplicates(df).drop([target_timestamp_str_internal_millis], axis=1)


class PandasFSBatchReader(TransformBatchReader):
    @to_string_date
    def read_by_event_date(self, start_date, end_date, date_format=default_date_format):
        return self._internal_read_event_time(to_millis(start_date, date_format), to_millis(end_date, date_format))

    @timestamp_handler
    def read_by_event_ts(self, start_event_time, end_event_time):
        return self._internal_read_event_time(start_event_time * 1000, end_event_time * 1000)

    @to_string_date
    def read_by_ingestion_date(self, start_date, end_date, date_format=default_date_format):
        return self._internal_read_ingestion_time(to_millis(start_date, date_format), to_millis(end_date, date_format))

    @timestamp_handler
    def read_by_ingestion_ts(self, start_ingestion_time, end_ingestion_time):
        return self._internal_read_ingestion_time(start_ingestion_time * 1000, end_ingestion_time * 1000)

    @to_string_date
    def point_in_time_join_by_date(self, entity_df, date_format=default_date_format):
        return self._internal_point_in_time_join(add_millis_columns_from_date(entity_df, date_format))

    @timestamp_handler
    def point_in_time_join_by_ts(self, entity_df):
        return self._internal_point_in_time_join(add_millis_columns_from_seconds(entity_df))

    def point_in_time_join_across_inputs_by_date(self, entity_df, input_list, date_format=default_date_format):
        df, ingest_cols, event_cols = self._internal_point_in_time_join_across_inputs(
            add_millis_columns_from_date(entity_df, date_format), input_list)
        df[ingest_cols + event_cols] = df[ingest_cols + event_cols].apply(str_formatted_date)
        return df

    def point_in_time_join_across_inputs_by_ts(self, entity_df, input_list):
        df, ingest_cols, event_cols = self._internal_point_in_time_join_across_inputs(
            add_millis_columns_from_seconds(entity_df), input_list)
        df[ingest_cols + event_cols] /= 1000
        return df

    def _internal_read_ingestion_time(self, start_ingestion_time, end_ingestion_time):
        if start_ingestion_time > end_ingestion_time:
            raise Exception("start ingestion time cannot be greater then end ingestion time")

        start_partition = datetime.fromtimestamp(start_ingestion_time / 1000).strftime(partition_format)
        end_partition = datetime.fromtimestamp(end_ingestion_time / 1000).strftime(partition_format)

        (transform_dir, partitions, options) = self._list_partitions()
        dirs_to_read = [f'{transform_dir}{partition}/*/*' for partition in partitions
                        if start_partition <= partition <= end_partition]
        df = read_files_to_pandas(dirs_to_read, options, self.features + self.entities +
                                  [ingest_time_str, event_time_str])
        return df[(df[ingest_time_str] <= end_ingestion_time) & (df[ingest_time_str] >= start_ingestion_time)]

    def _internal_read_event_time(self, start_event_time, end_event_time):
        if start_event_time > end_event_time:
            raise Exception("start event time cannot be greater then end event time")
        (path, options) = self.metadata_store.get_location_and_read_fs_options(self.namespace, self.name, self.version)
        df = read_files_to_pandas(f'{path}*/*/*', options, self.features + self.entities +
                                  [ingest_time_str, event_time_str])
        return df[(df[event_time_str] <= end_event_time) & (df[event_time_str] >= start_event_time)]

    def _internal_point_in_time_join(self, entity_df):
        (entity_df, final_df) = add_uuid(entity_df)
        final_df = point_in_time_join_helper(entity_df, final_df, self).reset_index(drop=True)
        return internal_point_in_time_join_return_handler(final_df)

    def _internal_point_in_time_join_across_inputs(self, entity_df, input_list):
        (entity_df, final_df) = add_uuid(entity_df)
        ingest_cols = []
        event_cols = []
        input_list.append(self)
        for reader in input_list:
            col_dict = {}
            prefix = f'{reader.namespace}_{reader.name}_{reader.version}'
            for col in reader.features:
                col_dict[col] = f'{prefix}.{col}'
            ingest_ts_col = f'{prefix}.{ingest_time_str}'
            event_ts_col = f'{prefix}.{event_time_str}'
            final_df = point_in_time_join_helper(entity_df, final_df, reader, col_dict).rename(columns={
                ingest_time_str: ingest_ts_col, event_time_str: event_ts_col})
            ingest_cols.append(ingest_ts_col)
            event_cols.append(event_ts_col)
        return internal_point_in_time_join_return_handler(final_df.reset_index(drop=True)), ingest_cols, event_cols

    def _list_partitions(self):
        (transform_dir, options) = self.metadata_store.get_location_and_read_fs_options(self.namespace, self.name,
                                                                                        self.version)
        fs, _, _ = fsspec.get_fs_token_paths(f'{transform_dir}', storage_options=options)

        dir_list = fs.ls(f'{transform_dir}')
        return transform_dir, [directory.split('/')[-1] for directory in dir_list], options


class PandasFSBatchWriter(TransformBatchWriter):
    def __init__(self,
                 metadata_store,
                 namespace,
                 name,
                 version,
                 code,
                 entities,
                 input_definition):
        super().__init__(metadata_store, namespace, name, version, code, entities, input_definition)

    def determine_features_and_entities(self, df):
        entities = {}
        features = {}
        for col in df.columns:
            internal_data_type = df_to_internal(df.dtypes[col])
            if col in self.entities:
                entities[col] = internal_data_type
            elif col != ingest_time_str and col != event_time_str:
                features[col] = internal_data_type
        return entities, features

    def write_df(self, df, ingest_timestamp, ingest_datetime, storage_options=None):
        storage_df = df.copy(deep=True)

        if event_time_str not in storage_df.columns:
            raise Exception(f"Missing {event_time_str} column. Please add event {event_time_str}")

        storage_df[ingest_time_str] = ingest_timestamp
        date_format = get_date_format(storage_options)
        if date_format[date_format_constant] == IngestionDateFormat.str_date:
            storage_df[event_time_str] = storage_df[event_time_str].apply(lambda x: to_millis(x, date_format[
                str_date_format_type_constant]))
        else:
            storage_df[event_time_str] *= 1000

        (path, options) = self.metadata_store.get_location_and_write_fs_options(self.namespace, self.name, self.version)
        path = f'{path}{ingest_datetime.strftime(partition_format)}/{str(uuid.uuid4())}/'

        file = fsspec.open_files(f'{path}', mode="wb", auto_mkdir=path.startswith("file://"), **options)
        pq.write_table(pa.Table.from_pandas(storage_df), f'{file[0].path}', filesystem=file[0].fs)
        return storage_df
