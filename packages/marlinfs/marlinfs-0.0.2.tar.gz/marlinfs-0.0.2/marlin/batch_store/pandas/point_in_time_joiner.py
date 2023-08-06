import uuid
from marlin.batch_store.pandas.utils import read_files_to_pandas, event_time_str
from marlin.batch_store.pandas.utils import ingest_time_str

uuid_str = 'uuid'
target_timestamp_str_internal_millis = 'target_timestamp_internal_millis'
target_timestamp_str = 'target_timestamp'


def add_uuid(df):
    df[uuid_str] = df.apply(lambda _: uuid.uuid4(), axis=1)
    return df, df.set_index(uuid_str)


def point_in_time_join_helper(entity_df, final_df, transform_batch_reader, rename_feature_dict=None):
    columns_to_read = transform_batch_reader.entities + transform_batch_reader.features + \
                      [event_time_str, ingest_time_str]
    (path, options) = transform_batch_reader.metadata_store.get_location_and_read_fs_options(
        transform_batch_reader.namespace, transform_batch_reader.name, transform_batch_reader.version)

    feature_df = read_files_to_pandas(f'{path}*/*/*', options, columns_to_read)

    feature_cols = transform_batch_reader.features
    if rename_feature_dict is not None:
        feature_df = feature_df.rename(columns=rename_feature_dict)
        feature_cols = rename_feature_dict.values()

    return point_in_time_join(entity_df, final_df, feature_df, transform_batch_reader.entities, feature_cols)


def point_in_time_join(entity_df, final_df, feature_df, entity_cols, feature_cols):
    output = create_point_in_time_feature_df(entity_df, feature_df, entity_cols)
    return join_feature_entity_with_main_entity(final_df, output, feature_cols)


def create_point_in_time_feature_df(entity_df, feature_df, entity_cols):
    entity_df_cols = entity_cols + [target_timestamp_str_internal_millis, uuid_str]
    join_df = entity_df[entity_df_cols].set_index(entity_cols).join(feature_df.set_index(entity_cols), how='inner')

    grouped_df = join_df.groupby(uuid_str)
    agg_df = grouped_df.apply(choose_feature).to_frame(name=event_time_str)
    agg_df[uuid_str] = agg_df.index

    join_df[uuid_str + "_temp"] = join_df[uuid_str]
    join_df[event_time_str + "_temp"] = join_df[event_time_str]
    final_join_df = join_df.drop(target_timestamp_str_internal_millis, 1).set_index([uuid_str, event_time_str])

    final_df = final_join_df.join(agg_df.set_index([uuid_str, event_time_str]), how='inner', rsuffix='+r')
    return final_df.reset_index(drop=True).rename(
        columns={uuid_str + "_temp": uuid_str, event_time_str + "_temp": event_time_str})


def choose_feature(df):
    return df.loc[df[event_time_str] <= df.iloc[0][target_timestamp_str_internal_millis]][event_time_str].max()


def join_feature_entity_with_main_entity(entity_df, point_in_time_feature_df, feature_cols):
    final_output_cols = [e for e in entity_df.columns] + list(feature_cols) + [ingest_time_str, event_time_str]
    indexed_point_in_time_feature_df = point_in_time_feature_df.set_index(uuid_str)
    return entity_df.join(indexed_point_in_time_feature_df, how='left', rsuffix='_r')[final_output_cols]
