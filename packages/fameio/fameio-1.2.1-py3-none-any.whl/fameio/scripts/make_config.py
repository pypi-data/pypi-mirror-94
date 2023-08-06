# !/usr/bin/env python
# -*- coding:utf-8 -*-

import pathlib as pt
import logging as log

from fameio.source.FieldValidator import FieldValidator, FieldType
from fameio.source.TimeSeriesManager import TimeSeriesManager
from fameio.source.tools import arg_handling_make_config, log_and_raise, set_up_logger
from fameio.source.loader import load_yaml
from fameio.source.FameTime import FameTime
from fameio.protobuf_definitions import InputFile_pb2
from fameio.protobuf_definitions import Contract_pb2


DEFAULT_CONFIG = {"log_level": "warning",
                  "output_file": "config.pb",
                  "log_file": None,
                  }


def set_general_properties(properties, proto):
    """Set the general simulation properties in the given proto_buffer"""
    for property_name, property_value in properties.items():
        if not hasattr(property_value, "keys"):
            setattr(proto, property_name, property_value)
        else:
            parent = getattr(proto, property_name)
            for child_property_name, child_property_value in property_value.items():
                if child_property_name == "StartTime" or child_property_name == "StopTime":
                    child_property_value = int(FameTime.convert_time_string_to_fame_time_step(child_property_value))
                setattr(parent, child_property_name, child_property_value)
        log.info("Set general properties for `{}`".format(property_name))


def update_field_values(pb_agent, fields, time_series_manager, field_validator):
    """Adds all fields in the given list to the given agent proto buffer"""
    if fields is not None:
        agent_type = pb_agent.className
        for field_name, field_value in fields.items():
            pb_field = pb_agent.field.add()
            pb_field.fieldName = field_name
            field_type = field_validator.get_field_type(agent_type, field_name)
            if field_validator.is_valid(agent_type, field_name, field_value):
                if field_type is FieldType.INTEGER:
                    pb_field.intValue = field_value
                elif field_type is FieldType.DOUBLE:
                    pb_field.doubleValue.extend([field_value])
                elif field_type is FieldType.ENUM:
                    pb_field.stringValue = field_value
                elif field_type is FieldType.TIME_SERIES:
                    if isinstance(field_value, str):
                        file_name = pt.Path(field_value).as_posix()
                        pb_field.seriesId = time_series_manager.save_get_time_series_id(file_name)
                    else:
                        pb_field.seriesId = time_series_manager.save_get_time_series_id(field_value)
                elif field_type is FieldType.DOUBLE_LIST:
                    for element in field_value:
                        pb_field.doubleValue.extend([element])
                else:
                    log_and_raise("FieldType '{}' not implemented.".format(field_type))
            else:
                log_and_raise("'{}' not allowed in field '{}' of agent {}".format(field_value, field_name, pb_agent.id))


def get_or_error(agent, param):
    """Gets given `param` from dictionary or raises error if field is missing"""
    try:
        return agent[param]
    except KeyError:
        log_and_raise("Cannot find '{}' in `agent` {}".format(param, agent))


def set_agents_and_time_series(agent_list, proto_buffer, field_validator):
    """
    Iterates through all agents, adds them and all of their fields to the given proto buffer and also
    adds all referenced files as time series to the proto_buffer. Ensures proper field parameterization and format.
    """
    time_series_manager = TimeSeriesManager()
    for agent in agent_list:
        agent = convert_keys_to_lower(agent)
        pb_agent = proto_buffer.Agent.add()
        pb_agent.className = get_or_error(agent, "type")
        pb_agent.id = get_or_error(agent, "id")
        if "attributes" in agent:
            fields = agent.get("attributes")
            update_field_values(pb_agent, fields, time_series_manager, field_validator)
        log.info("Set `Attributes` for agent `{}` with ID `{}`".format(pb_agent.className, pb_agent.id))
    time_series_manager.add_time_series_to_proto_buffer(proto_buffer)


def convert_keys_to_lower(agent):
    """Returns given dictionary with `keys` in lower case"""
    return {keys.lower(): value for keys, value in agent.items()}


def set_contracts(contracts, proto_buffer):
    """Adds all contracts in the given list to the given proto buffer"""
    valid_keys = [field.name for field in Contract_pb2._PROTOCONTRACT.fields]
    for contract in contracts:
        pb_contract = proto_buffer.Contract.add()
        for key, value in contract.items():
            key = get_valid_key(key, valid_keys)
            setattr(pb_contract, key, value)
    log.info("Added contracts to protobuf file.")


def get_valid_key(key, valid_keys):
    """Returns an entry from given `valid_keys` with an case insensitive match of `key`"""
    for valid_key in valid_keys:
        if key.lower() == valid_key.lower():
            return valid_key
    log_and_raise("Key `{}` not in list of valid keys `{}`.".format(key, valid_keys))


def write_protobuf_to_disk(output_file, proto_input_data):
    """Writes given `protobuf_input_data` in `output_file` to disk"""
    f = open(output_file, "wb")
    f.write(proto_input_data.SerializeToString())
    f.close()
    log.info("Saved protobuf file `{}` to disk".format(output_file))


def run(file, config=DEFAULT_CONFIG):
    """Executes the main workflow for the building of a FAME configuration file"""
    set_up_logger(level=config["log_level"], file_name=config["log_file"])

    config_data = load_yaml(file)
    validator = FieldValidator(config_data["Schema"])
    proto_input_data = InputFile_pb2.InputData()
    set_general_properties(config_data["GeneralProperties"], proto_input_data)
    set_agents_and_time_series(config_data["Agents"], proto_input_data, validator)

    contract_list = config_data["Contracts"]
    set_contracts(contract_list, proto_input_data)

    write_protobuf_to_disk(config["output_file"], proto_input_data)

    log.info("Completed conversion of all input in `{}` to protobuf file `{}`".format(file, config["output_file"]))


if __name__ == '__main__':
    input_file, run_config = arg_handling_make_config(DEFAULT_CONFIG)
    run(input_file, run_config)
