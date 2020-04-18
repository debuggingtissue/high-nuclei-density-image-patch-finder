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
                                resolution_level,
                                overlapping_percentage,
                                window_size,
                                patching_area_x=None,
                                patching_area_y=None,
                                patching_area_width=None,
                                patching_area_height=None):
    img = openslide.OpenSlide(full_image_path)

    has_specific_patching_area = patching_area_x is not None and patching_area_y is not None and patching_area_width is not None and patching_area_height is not None

    if has_specific_patching_area:
        start_position_x = int(patching_area_x)
        start_position_y = int(patching_area_y)
        width, height = int(patching_area_width), int(patching_area_height)
    else:
        start_position_x = 0
        start_position_y = 0
        width, height = img.level_dimensions[resolution_level]


    x_start_positions = get_start_positions(start_position_x, width, height, window_size, enums.Axis.X,
                                            overlapping_percentage)
    y_start_positions = get_start_positions(start_position_y, width, height, window_size, enums.Axis.Y,
                                            overlapping_percentage)

    print(x_start_positions)
    print(y_start_positions)

    total_number_of_patches = len(x_start_positions) * len(y_start_positions)
    tile_number = 1

    for x_index, x_start_position in enumerate(x_start_positions):
        for y_index, y_start_position in enumerate(y_start_positions):

            x_end_position = min(width + start_position_x, x_start_position + window_size)
            y_end_position = min(height + start_position_y, y_start_position + window_size)
            patch_width = x_end_position - x_start_position
            patch_height = y_end_position - y_start_position

            print(start_position_x)
            print(start_position_y)
            print(width)
            print(height)
            print(patch_width)
            print(patch_height)

            print("==============                                                                         ")

            is_image_patch_size_equal_to_window_size = ((patch_height == window_size) and (patch_width == window_size))
            if not is_image_patch_size_equal_to_window_size:
                continue

            SVS_level_ratio = int(
                svs_utils.get_SVS_level_ratio(img, enums.ResolutionLevel.LEVEL_0_BASE, resolution_level))
            patch = img.read_region((x_start_position * SVS_level_ratio, y_start_position * SVS_level_ratio),
                                    resolution_level,
                                    (patch_width, patch_height))
            patch.load()
            patch_rgb = Image.new("RGB", patch.size, (255, 255, 255))
            patch_rgb.paste(patch, mask=patch.split()[3])

            print("\n")
            print("Patch data", x_start_position, y_start_position, resolution_level, patch_width, patch_height)
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
                                         case_id, resolution_level, x_start_position,
                                         y_start_position, patch_width, patch_height))

            patch_rgb.save(output_image_name)
            print("Tile", tile_number, "/", total_number_of_patches, "created")
            tile_number = tile_number + 1
