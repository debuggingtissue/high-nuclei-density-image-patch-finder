import argparse
from utils import path_utils, image_patch_file_name_parser
from mirzaevinom_nuclei_segmenter import predict
import shutil

def output_image_patch_with_highest_predicted_nuclei_count(image_patches_path, output_diretory_path):
    image_patch_paths = path_utils.create_full_paths_to_files_in_directory_path(image_patches_path)
    image_patch_path_with_highest_nuclei_count = None
    highest_nuclei_count = 0
    for image_patch_path in image_patch_paths:
        image_patch_file_name = image_patch_path.split('/')[-1]
        predicted_nuclei_count = int(image_patch_file_name_parser.parse_image_patch_for_nuclei_count_prediction(image_patch_file_name))
        if predicted_nuclei_count >= highest_nuclei_count:
            image_patch_path_with_highest_nuclei_count = image_patch_path
            highest_nuclei_count = predicted_nuclei_count

    image_patch_file = image_patch_path_with_highest_nuclei_count.split('/')[-1]
    new_image_patch_path = output_diretory_path + "/" + image_patch_file


    shutil.move(image_patch_path_with_highest_nuclei_count, new_image_patch_path)


parser = argparse.ArgumentParser(description="Finding the image patch with the highest nuclei density for each case")
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

    path_to_image_patches = case_directory_path + "/" + "images_original"

    case_id = case_directory_path.split('/')[-1]
    case_id_output_path = output_folder_path + "/" + case_id
    path_utils.create_directory_if_directory_does_not_exist_at_path(case_id_output_path)

    output_image_patch_with_highest_predicted_nuclei_count(path_to_image_patches, case_id_output_path)

