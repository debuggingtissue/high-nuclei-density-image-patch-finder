import argparse
import os
from os.path import isfile, join
from PIL import Image, ImageDraw
import openslide
from utils import path_utils
from utils import enums
from utils import svs_utils, image_patch_predictions_constants, image_patch_file_name_constants
import csv


def create_jpeg_thumbnail_of_wsi(full_image_name_path):
    img = openslide.OpenSlide(full_image_name_path)
    thumbnail = img.associated_images["thumbnail"]

    return thumbnail


def draw_prediction_annotations_onto_thumbnail(svs_image, thumbnail, full_cvs_path, output_directory_path,
                                               accuracy_percentage_threshold):
    TINT_COLOR = (0, 255, 0)  # Black
    TRANSPARENCY = .20  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)
    print("yO")
    case_id = None
    with open(full_cvs_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            saliency_prediction = float(row[image_patch_predictions_constants.PREDICTION_VALUE_SALIENT])
            case_id = row[image_patch_file_name_constants.CASE_ID]
            print(saliency_prediction)

            if saliency_prediction > accuracy_percentage_threshold:
                print("Wut")
                resolution_level = int(row[image_patch_file_name_constants.RESOLUTION_LEVEL])

                x_coordinate = svs_utils.scale(int(row[image_patch_file_name_constants.X_COORDINATE]), resolution_level,
                                               enums.ResolutionLevel.THUMBNAIL, svs_image)
                y_coordinate = svs_utils.scale(int(row[image_patch_file_name_constants.Y_COORDINATE]), resolution_level,
                                               enums.ResolutionLevel.THUMBNAIL, svs_image)

                print(x_coordinate)
                print(y_coordinate)

                width = svs_utils.scale(int(row[image_patch_file_name_constants.WIDTH]), resolution_level,
                                        enums.ResolutionLevel.THUMBNAIL, svs_image)
                height = svs_utils.scale(int(row[image_patch_file_name_constants.HEIGHT]), resolution_level,
                                         enums.ResolutionLevel.THUMBNAIL, svs_image)

                overlay = Image.new('RGBA', thumbnail.size, TINT_COLOR + (0,))
                draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
                draw.rectangle(((x_coordinate, y_coordinate), (x_coordinate + width, y_coordinate + height)),
                               fill=TINT_COLOR + (OPACITY,))

                thumbnail = Image.alpha_composite(thumbnail, overlay)

    thumbnail = thumbnail.convert("RGB")
    thumbnail.save(output_directory_path + case_id + "_annotated.jpeg", 'JPEG')


parser = argparse.ArgumentParser(description='Saliency visualization.')
parser.add_argument("-svs", "--svs_input_folder_path", type=str, help=" The path to the SVS input folder.",
                    required=True)
parser.add_argument("-csv", "--csv_input_folder_path", type=str, help="The path to the CSV input folder.",
                    required=True)
parser.add_argument("-o", "--output_folder_path", type=str, help="The path to the output folder."
                                                                 " If output folder doesn't exists at runtime "
                                                                 "the script will create it.",
                    required=True)
parser.add_argument("-apt", "--accuracy_percentage_threshold", type=float,
                    help="Accuracy percentage threshold for showing annotations",
                    required=True)

args = parser.parse_args()

svs_input_folder_path = args.svs_input_folder_path
csv_input_folder_path = args.csv_input_folder_path
output_folder_path = args.output_folder_path
accuracy_percentage_threshold = args.accuracy_percentage_threshold

path_utils.halt_script_if_path_does_not_exist(svs_input_folder_path)
path_utils.halt_script_if_path_does_not_exist(csv_input_folder_path)

path_utils.create_directory_if_directory_does_not_exist_at_path(output_folder_path)

full_tcga_download_directory_paths = path_utils.create_full_paths_to_directories_in_directory_path(
    svs_input_folder_path)

full_image_patch_data_dict_paths = path_utils.create_full_paths_to_files_in_directory_path(csv_input_folder_path)

for full_tcga_download_directories_path_index, full_tcga_download_directory_path in enumerate(
        full_tcga_download_directory_paths):
    full_image_name_paths = path_utils.create_full_paths_to_files_in_directory_path(full_tcga_download_directory_path)
    print("hey")
    image_name = full_image_name_paths[0].split('/')[-1][:-4]
    output_path = output_folder_path + '/' + image_name + '/'
    path_utils.create_directory_if_directory_does_not_exist_at_path(output_path)
    thumbnail = create_jpeg_thumbnail_of_wsi(full_image_name_paths[0])
    thumbnail = thumbnail.convert("RGB")
    thumbnail.save(output_path + image_name + "_original.jpeg", 'JPEG')
    thumbnail = thumbnail.convert("RGBA")
    svs_image = svs_utils.get_svs_image_of_wsi_from_path(full_image_name_paths[0])
    draw_prediction_annotations_onto_thumbnail(svs_image,
                                               thumbnail,
                                               full_image_patch_data_dict_paths[
                                                   full_tcga_download_directories_path_index],
                                               output_path,
                                               accuracy_percentage_threshold)
