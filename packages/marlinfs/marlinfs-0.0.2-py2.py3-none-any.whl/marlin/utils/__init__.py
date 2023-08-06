from marlin.marlin_service_pb2 import DataType


def dict_set_helper(dict, field):
    for (key, val) in dict.items():
        field[key] = val


def dict_set_helper_with_data_type(dict, field, map_for_data_type):
    for (key, val) in dict.items():
        set_field(map_for_data_type[key], val, field[key])


def set_field(data_type, val, field_to_set):
    if DataType.INTEGER == data_type:
        field_to_set.int_val = val
    elif DataType.LONG == data_type:
        field_to_set.long_val = val
    elif DataType.DOUBLE == data_type:
        field_to_set.double_val = val
    elif DataType.BOOLEAN == data_type:
        field_to_set.bool_val = val
    elif DataType.STRING == data_type:
        field_to_set.string_val = val
    else:
        raise Exception(f'Unkown data type {data_type} for field {field_to_set} and value {val}')


def to_feature_dict(features, schema):
    feature_dict = {}
    for fk, fv in features.features.items():
        feature_dict[fk] = get_feature_value(fv, schema.features[fk])
    return feature_dict


def get_feature_value(fv, data_type):
    if DataType.INTEGER == data_type:
        return fv.int_val
    elif DataType.LONG == data_type:
        return fv.long_val
    elif DataType.DOUBLE == data_type:
        return fv.double_val
    elif DataType.BOOLEAN == data_type:
        return fv.bool_val
    elif DataType.STRING == data_type:
        return fv.string_val
    else:
        raise Exception(f'Unknown data type {data_type} for field {fv}')
