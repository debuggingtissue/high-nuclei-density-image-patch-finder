from os.path import isfile, join
from PIL import Image
import openslide
from utils import path_utils, enums, svs_utils, image_patch_file_name_builder

compression_factor = 1
Image.MAX_IMAGE_PIXELS = 1e10


def get_start_positions(start_position, width, height, window_size, axis, overlapping_percentage):
    start_positions = []

    start_positions.append(start_position)
    first_start_position = start_position

    dimension = width if axis == enums.Axis.X else height

    while not (start_position + (window_size * (1 - overlapping_percentage))) > dimension + first_start_position:
        start_position = start_position + (window_size * (1 - overlapping_percentage))
        start_positions.append(int(start_position))

    return start_positions


def split_to_jpeg_image_patches(full_image_path,
                                full_output_path,
                                to_resolution_level,
                                overlapping_percentage,
                                window_size,
                                from_resolution_level=enums.ResolutionLevel.LEVEL_0_BASE,
                                patching_area_x=None,
                                patching_area_y=None,
                                patching_area_width=None,
                                patching_area_height=None):
    img = openslide.OpenSlide(full_image_path)

    has_specific_patching_area = patching_area_x is not None and patching_area_y is not None and patching_area_width is not None and patching_area_height is not None
    if has_specific_patching_area:
        original_start_position_x = int(patching_area_x)
        original_start_position_y = int(patching_area_y)
        width, height = int(patching_area_width), int(patching_area_height)
    else:
        original_start_position_x = 0
        original_start_position_y = 0
        width, height = img.level_dimensions[from_resolution_level]


    print(width)
    print(height)
    print(window_size)

    original_start_position_x_label = int(svs_utils.scale(
        int(original_start_position_x), from_resolution_level, to_resolution_level, img))
    original_start_position_y_label = int(svs_utils.scale(int(original_start_position_y), from_resolution_level, to_resolution_level, img))
    width = int(svs_utils.scale(int(width), from_resolution_level, to_resolution_level, img))
    height = int(svs_utils.scale(int(height), from_resolution_level, to_resolution_level, img))


    x_start_positions_labels = get_start_positions(original_start_position_x_label, width, height, window_size, enums.Axis.X,
                                            overlapping_percentage)
    y_start_positions_label = get_start_positions(original_start_position_y_label, width, height, window_size, enums.Axis.Y,
                                            overlapping_percentage)

    print(x_start_positions_labels)
    print(y_start_positions_label)
    print(width)
    print(height)
    print(window_size)

    total_number_of_patches = len(x_start_positions_labels) * len(y_start_positions_label)
    tile_number = 1

    for x_index, x_start_position in enumerate(x_start_positions_labels):
        for y_index, y_start_position in enumerate(y_start_positions_label):

            x_end_position = min(original_start_position_x + width, x_start_position + window_size)
            y_end_position = min(original_start_position_y + height, y_start_position + window_size)
            patch_width = x_end_position - x_start_position
            patch_height = y_end_position - y_start_position

            is_image_patch_size_equal_to_window_size = ((patch_height == window_size) and (patch_width == window_size))
            if not is_image_patch_size_equal_to_window_size:
                continue

            print("==============")

            print(x_start_position)
            print(y_start_position)
            print(patch_width)
            print(patch_height)

            print("==============")
            #must always convert to resolution 0 when doing patch extraction
            svs_x_value = int(svs_utils.scale(x_start_position, to_resolution_level, from_resolution_level, img))
            svs_y_value = int(svs_utils.scale(y_start_position, to_resolution_level, from_resolution_level, img))
            print("returmed ratio")
            print(svs_x_value)
            print(svs_y_value)
            patch = img.read_region((svs_x_value, svs_y_value),
                                    to_resolution_level,
                                    (patch_width, patch_height))
            patch.load()
            patch_rgb = Image.new("RGB", patch.size, (255, 255, 255))
            patch_rgb.paste(patch, mask=patch.split()[3])

            print("\n")
            print("Patch data", x_start_position, y_start_position, to_resolution_level, patch_width, patch_height)
            print("Tile size for tile number " + str(tile_number) + ":" + str(patch.size))

            # compress the image
            # patch_rgb = patch_rgb.resize(
            #    (int(patch_rgb.size[0] / compression_factor), int(patch_rgb.size[1] / compression_factor)),
            #    Image.ANTIALIAS)

            # save the image

            case_id = full_image_path.split('/')[-1][:-4]

            output_subfolder = join(full_output_path, case_id)
            path_utils.create_directory_if_directory_does_not_exist_at_path(output_subfolder)

            output_image_name = join(output_subfolder,
                                     image_patch_file_name_builder.build_image_patch_file_name(
                                         case_id, to_resolution_level, x_start_position,
                                         y_start_position, patch_width, patch_height))

            patch_rgb.save(output_image_name)
            print("Tile", tile_number, "/", total_number_of_patches, "created")
            tile_number = tile_number + 1
