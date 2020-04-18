import argparse
from utils import path_utils
from mirzaevinom_nuclei_segmenter import predict

parser = argparse.ArgumentParser(description="Finding")
parser.add_argument("-i", "--input_folder_path", type=str, help="The path to the input folder.", required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)
args = parser.parse_args()

input_folder_path = args.input_folder_path
output_folder_path = args.output_folder_path

path_utils.halt_script_if_path_does_not_exist(input_folder_path)
path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)
case_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(input_folder_path)

for case_directory_path in case_directory_paths:
    full_image_patch_paths_in_a_single_case = path_utils.create_full_paths_to_files_in_directory_path(
        case_directory_path)

    image_patch_with_highest_nuclei_absolute_path = None
    highest_nuclei_count = 0

    for full_image_patch_path in full_image_patch_paths_in_a_single_case:

        nuclei_count_prediction_in_image_patch = predict.nuclei_count_in_image_patch()
        if nuclei_count_prediction_in_image_patch > highest_nuclei_count:
            image_patch_with_highest_nuclei_absolute_path = full_image_patch_path
            highest_nuclei_count = nuclei_count_prediction_in_image_patch

    output_path = output_folder_path + '/'

    output_image_patch_with_highest_nuclei_count(output_folder_path,
                                                 case_directory_path,
                                                 image_patch_with_highest_nuclei_absolute_path)
# output
# folder for each case containing image with the most nuclei
