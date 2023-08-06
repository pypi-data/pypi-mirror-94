import csv
import geojson
import json
import yaml
from base64 import b64decode, b64encode

from ..exceptions import CrossComputeExecutionError
from ..macros import get_plain_value, parse_number, parse_number_safely
from ..symmetries import cache


class FairDumper(yaml.SafeDumper):
    # https://ttl255.com/yaml-anchors-and-aliases-and-how-to-disable-them

    def ignore_aliases(self, data):
        return True

    def represent_str(self, data):
        parent_instance = super()
        return parent_instance.represent_scalar(
            'tag:yaml.org,2002:str', data, style='|',
        ) if '\n' in data else parent_instance.represent_str(data)


FairDumper.add_representer(str, FairDumper.represent_str)


def render_object(raw_object, as_json=False):
    if as_json:
        text = json.dumps(raw_object)
    else:
        text = '---\n' + yaml.dump(
            raw_object, Dumper=FairDumper, sort_keys=False)
    return text.strip()


def save_json(target_path, value_by_id):
    json.dump(value_by_id, open(target_path, 'wt'))


def save_text(target_path, value):
    open(target_path, 'wt').write(value)


def save_binary_bin(target_path, value, variable_id, value_by_id_by_path):
    return save_binary(target_path, value)


def save_binary_base64(target_path, value):
    save_binary(target_path, b64decode(value))


def save_binary(target_path, value):
    open(target_path, 'wb').write(value)


def save_text_json(target_path, value, variable_id, value_by_id_by_path):
    value_by_id_by_path[target_path][variable_id] = value


def save_text_txt(target_path, value, variable_id, value_by_id_by_path):
    save_text(target_path, value)


def save_number_json(target_path, value, variable_id, value_by_id_by_path):
    try:
        value = parse_number(value)
    except ValueError:
        raise CrossComputeExecutionError({
            'variable': f'could not save {variable_id} as a number'})
    value_by_id_by_path[target_path][variable_id] = value


def save_markdown_md(target_path, value, variable_id, value_by_id_by_path):
    save_text(target_path, value)


def save_table_csv(target_path, value, variable_id, value_by_id_by_path):
    try:
        columns = value['columns']
        rows = value['rows']
        with open(target_path, 'wt') as target_file:
            csv_writer = csv.writer(target_file)
            csv_writer.writerow(columns)
            csv_writer.writerows(rows)
    except (KeyError, csv.Error):
        raise CrossComputeExecutionError({
            'variable': f'could not save {variable_id} as a table csv'})


def save_image_png(target_path, value, variable_id, value_by_id_by_path):
    save_binary_base64(target_path, value)


def save_image_jpg(target_path, value, variable_id, value_by_id_by_path):
    save_binary_base64(target_path, value)


def save_map_geojson(target_path, value, variable_id, value_by_id_by_path):
    geojson.dump(value, open(target_path, 'wt'))


def save_electricity_network_json(
        target_path, value, variable_id, value_by_id_by_path):
    save_json(target_path, value)


def load_json(source_path):
    return json.load(open(source_path, 'rt'))


def load_text(source_path):
    return open(source_path, 'rt').read()


def load_binary_base64(source_path):
    variable_value = load_binary(source_path)
    variable_value = b64encode(variable_value)
    return variable_value.decode('utf-8')


def load_binary_bin(source_path, variable_id):
    return load_binary(source_path)


def load_binary(source_path):
    return open(source_path, 'rb').read()


@cache
def load_value_json(source_path, variable_id):
    d = json.load(open(source_path, 'rt'))
    try:
        variable_value = d[variable_id]
    except KeyError:
        raise CrossComputeExecutionError({
            'variable': f'could not load {variable_id} from {source_path}'})
    return variable_value


def load_text_json(source_path, variable_id):
    return load_value_json(source_path, variable_id)


def load_text_txt(source_path, variable_id):
    return load_text(source_path)


def load_number_json(source_path, variable_id):
    value = load_value_json(source_path, variable_id)
    try:
        value = parse_number(value)
    except ValueError:
        raise CrossComputeExecutionError({
            'variable': f'could not load {variable_id}={value} as a number'})
    return value


def load_markdown_md(source_path, variable_id):
    return load_text(source_path)


def load_table_csv(source_path, variable_id):
    csv_reader = csv.reader(open(source_path, 'rt'))
    columns = next(csv_reader)
    rows = [[parse_number_safely(_) for _ in row] for row in csv_reader]
    return {'columns': columns, 'rows': rows}


def load_image_png(source_path, variable_id):
    return load_binary_base64(source_path)


def load_image_jpg(source_path, variable_id):
    return load_binary_base64(source_path)


def load_map_geojson(source_path, variable_id):
    try:
        variable_value = geojson.load(open(source_path, 'rt'))
    except ValueError:
        raise CrossComputeExecutionError({
            'variable': f'could not load {variable_id} as a map geojson'})
    # TODO: Consider whether to assert FeatureCollection
    return get_plain_value(variable_value)


def load_electricity_network_json(source_path, variable_id):
    return load_json(source_path)


SAVE_BY_EXTENSION_BY_VIEW = {
    'text': {
        '.txt': save_text_txt,
        '.json': save_text_json,
    },
    'number': {
        '.json': save_number_json,
    },
    'markdown': {
        '.md': save_markdown_md,
    },
    'table': {
        '.csv': save_table_csv,
    },
    'image': {
        '.png': save_image_png,
        '.jpg': save_image_jpg,
    },
    'map': {
        '.geojson': save_map_geojson,
        '.json': save_map_geojson,
    },
    'electricity-network': {
        '.json': save_electricity_network_json,
    },
    'file': {
        '.bin': save_binary_bin,
        '.*': save_binary_bin,
    },
}


# TODO: Consider separating these views into different packages
LOAD_BY_EXTENSION_BY_VIEW = {
    'text': {
        '.txt': load_text_txt,
        '.json': load_text_json,
    },
    'number': {
        '.json': load_number_json,
    },
    'markdown': {
        '.md': load_markdown_md,
    },
    'table': {
        '.csv': load_table_csv,
    },
    'image': {
        '.png': load_image_png,
        '.jpg': load_image_jpg,
    },
    'map': {
        '.geojson': load_map_geojson,
        '.json': load_map_geojson,
    },
    'electricity-network': {
        '.json': load_electricity_network_json,
    },
    'file': {
        '.bin': load_binary_bin,
        '.*': load_binary_bin,
    },
}
