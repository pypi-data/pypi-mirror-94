import fsspec
from marlin.marlin_service_pb2 import DataType
import numpy as np
import pandas as pd

event_time_str = 'event_timestamp'
ingest_time_str = 'ingestion_timestamp'


def drop_duplicates(df, should_drop_duplicates=True):
    if should_drop_duplicates:
        return df.drop_duplicates()
    else:
        return df


def read_files_to_pandas(dirs_to_read, options, columns):
    fs, _, paths = fsspec.get_fs_token_paths(dirs_to_read, storage_options=options)

    if columns is None:
        return fs.read_parquet(path=paths).to_pandas()
    else:
        return fs.read_parquet(path=paths, columns=columns).to_pandas()


def df_to_internal(dtype):
    d_type = dtype.type
    if d_type == np.int8 or d_type == np.int16 or d_type == np.uint8 or d_type == np.uint16:
        return DataType.INTEGER
    if d_type == np.int32 or d_type == np.int64 or d_type == np.uint32 or d_type == np.uint64:
        return DataType.LONG
    if d_type == np.bool_:
        return DataType.BOOLEAN
    if d_type == np.object_ or d_type == pd.StringDtype:
        return DataType.STRING
    if d_type == np.float32 or d_type == np.float64 or np.float_:
        return DataType.DOUBLE
    raise Exception(f'Unknown data type supplied {dtype.type}')
