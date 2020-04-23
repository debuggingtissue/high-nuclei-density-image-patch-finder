import argparse
from utils import svs_utils, image_patch_predictions_constants, image_patch_file_name_constants, path_utils, \
    svs_splitter, enums

import csv


def get_image_patch_with_highest_saliency_data_dict(full_csv_file_path):
    case_id = None
    print(full_csv_file_path)
    with open(full_csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        maximum_prediction_value = 0
        maximum_prediction_row = None
        for row in reader:

            saliency_prediction = float(row[image_patch_predictions_constants.PREDICTION_VALUE_SALIENT])
            if saliency_prediction > maximum_prediction_value:
                maximum_prediction_value = saliency_prediction
                maximum_prediction_row = row

        print(maximum_prediction_row)
        resolution_level = int(maximum_prediction_row[image_patch_file_name_constants.RESOLUTION_LEVEL])
        print(resolution_level)
        print(to_resolution_level)
        x_coordinate = int(maximum_prediction_row[image_patch_file_name_constants.X_COORDINATE])
        y_coordinate = int(maximum_prediction_row[image_patch_file_name_constants.Y_COORDINATE])
        patching_area_width = int(maximum_prediction_row[image_patch_file_name_constants.WIDTH])
        patching_area_height = int(maximum_prediction_row[image_patch_file_name_constants.HEIGHT])

        image_patch_with_highest_saliency_data_dict = {}
        image_patch_with_highest_saliency_data_dict[image_patch_file_name_constants.X_COORDINATE] = x_coordinate
        image_patch_with_highest_saliency_data_dict[image_patch_file_name_constants.Y_COORDINATE] = y_coordinate
        image_patch_with_highest_saliency_data_dict[image_patch_file_name_constants.WIDTH] = patching_area_width
        image_patch_with_highest_saliency_data_dict[image_patch_file_name_constants.HEIGHT] = patching_area_height
        image_patch_with_highest_saliency_data_dict[image_patch_file_name_constants.RESOLUTION_LEVEL] = resolution_level

        return image_patch_with_highest_saliency_data_dict


parser = argparse.ArgumentParser(
    description="Generate high resolution image patches of an image patch at a lower resolution")
parser.add_argument("-svs", "--svs_input_folder_path", type=str, help=" The path to the SVS input folder.",
                    required=True)
parser.add_argument("-csv", "--csv_input_folder_path", type=str, help="The path to the CSV input folder.",
                    required=True)

parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)

parser.add_argument("-r", "--resolution_level", type=int, default=0, choices=[0, 1, 2, 3],

                    help="Resolution level for image to be split."
                         " Low level equals high resolution, lowest level is 0. Choose between {0, 1, 2, 3}."
                         " Default value is 0.")

parser.add_argument("-op", "--overlap_percentage", type=int, default=0,
                    help="Overlapping percentage between patches."
                         " Default value is 0.")

parser.add_argument("-ws ", "--window_size", type=int, default=10000,
                    help="Size for square window"
                         " Default value is 10000.")

args = parser.parse_args()

svs_input_folder_path = args.svs_input_folder_path
csv_input_folder_path = args.csv_input_folder_path
output_folder_path = args.output_folder_path
to_resolution_level = int(args.resolution_level)
overlapping_percentage = float("{0:.2f}".format(args.overlap_percentage / 100))
window_size = args.window_size

path_utils.halt_script_if_path_does_not_exist(svs_input_folder_path)
path_utils.halt_script_if_path_does_not_exist(csv_input_folder_path)

path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

full_tcga_download_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    svs_input_folder_path)

full_image_patch_data_dict_paths = path_utils.create_full_paths_to_files_in_directory_path(csv_input_folder_path)

for full_tcga_download_directories_path_index, full_tcga_download_directory_path in enumerate(
        full_tcga_download_directory_paths):
    full_image_name_paths = path_utils.create_full_paths_to_files_in_directory_path(full_tcga_download_directory_path)
    # there might be more than one image in a tcga download directory path (TO-DO: improve current solution)
    first_image_name_path = full_image_name_paths[0]

    image_name = first_image_name_path.split('/')[-1][:-4]
    full_csv_file_path = full_image_patch_data_dict_paths[
        full_tcga_download_directories_path_index]


    svs_image = svs_utils.get_svs_image_of_wsi_from_path(first_image_name_path)
    image_patch_with_highest_saliency_data_dict = get_image_patch_with_highest_saliency_data_dict(full_csv_file_path)
    print(image_patch_with_highest_saliency_data_dict)
    print("HEY")

    svs_splitter.split_to_jpeg_image_patches(first_image_name_path,
                                             output_folder_path,
                                             to_resolution_level,
                                             overlapping_percentage,
                                             window_size,
                                             from_resolution_level=image_patch_with_highest_saliency_data_dict[
                                                 image_patch_file_name_constants.RESOLUTION_LEVEL],
                                             patching_area_x=image_patch_with_highest_saliency_data_dict[
                                                 image_patch_file_name_constants.X_COORDINATE],
                                             patching_area_y=image_patch_with_highest_saliency_data_dict[
                                                 image_patch_file_name_constants.Y_COORDINATE],
                                             patching_area_width=image_patch_with_highest_saliency_data_dict[
                                                 image_patch_file_name_constants.WIDTH],
                                             patching_area_height=image_patch_with_highest_saliency_data_dict[
                                                 image_patch_file_name_constants.HEIGHT])
