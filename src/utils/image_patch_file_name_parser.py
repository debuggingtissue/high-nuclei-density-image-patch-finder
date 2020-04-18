from .image_patch_file_name_constants import *


def parse_image_patch_file_name_to_dict(image_patch_file_name):
    file_name_without_file_type = image_patch_file_name[:-4]
    file_properties_key_value_pairs = file_name_without_file_type.split(SEPARATOR)
    dict = {}
    for file_property_key_value_pair in file_properties_key_value_pairs:
        file_properties_key_value_pairs_separated = file_property_key_value_pair.split(EQUAL)
        key = file_properties_key_value_pairs_separated[0]
        value = file_properties_key_value_pairs_separated[-1]
        dict[key] = value
    return dict
