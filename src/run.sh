#!/bin/bash
source config.sh

###################################
#               RUN               #
###################################

#source "${S0_VIRTUAL_ENV_36}/bin/activate"
#python3.6 1_split_svs_images_to_image_patches.py \
#  -i $S1_SPLIT_SVS_S0_INPUT_DIRECTORY_PATH \
#  -o $S1_SPLIT_SVS_OUTPUT_DIRECTORY_PATH \
#  -r $S1_RESOLUTION_LEVEL \
#  -op $S1_OVERLAP_PERCENTAGE \
#  -ws $S1_WINDOW_SIZE
#
#python3.6 2_preprocess_image_patches.py \
#  -i $S2_PREPROCESS_IMAGE_PATCHES_INPUT_DIRECTORY_PATH \
#  -o $S2_PREPROCESS_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH \
#  -fc $S2_FIRST_CENTERMOST_CROP_SIZE \
#  -ds $S2_DOWNSCALED_SIZE \
#  -sc $S2_SECOND_CENTERMOST_CROP_SIZE
#
#source "${S0_VIRTUAL_ENV_27}/bin/activate"
#python 3_predict_saliency_for_image_patches.py \
#  -i $S3_PREDITCT_SALIENCY_INPUT_DIRECTORY_PATH \
#  -o $S3_PREDITCT_SALIENCY_OUTPUT_DIRECTORY_PATH
#
#source "${S0_VIRTUAL_ENV_36}/bin/activate"
#python3.6 4_create_saliency_visualization.py \
#  -svs $S4_CREATE_SALIENCY_VISUALIZATION_SVS_INPUT_DIRECTORY_PATH \
#  -csv $S4_CREATE_SALIENCY_VISUALIZATION_CSV_INPUT_DIRECTORY_PATH \
#  -o $S4_CREATE_SALIENCY_VISUALIZATION_OUTPUT_DIRECTORY_PATH \
#  -apt $S4_CREATE_SALIENCY_ACCURACY_PERCENTAGE_THRESHOLD
#
#python3.6 pipeline/5_convert_salient_image_patches_to_high_resolution_image_patches.py \
#  -svs $S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_SVS_INPUT_DIRECTORY \
#  -csv $S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_CSV_INPUT_DIRECTORY \
#  -o $S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH \
#  -r $S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_TARGET_RESOLUTION_LEVEL \
#  -op $S5_CREATE_HIGH_RESOLUTION_IMAGE_OVERLAP_PERCENTAGE \
#  -ws $S5_CREATE_HIGH_RESOLUTION_IMAGE_WINDOW_SIZE

#source "${S0_VIRTUAL_ENV_36}/bin/activate"
#python3.6 pipeline/6_preprocess_high_resolution_image_patches.py \
#  -i $S6_PREPROCESS_HIGH_RESOLUTION_IMAGE_PATCHES_INPUT_DIRECTORY_PATH \
#  -o $S6_PREPROCESS_HIGH_RESOLUTION_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH \
#  -ds $S6_HIGH_RESOLUTION_IMAGE_PATCH_DOWNSCALED_SIZE
#
#python3.6 pipeline/7_reorganize_directories_for_segmentor.py \
#  -i $S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_INPUT_DIRECTORY_PATH \
#  -o $S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_OUTPUT_DIRECTORY_PATH

source "${S0_VIRTUAL_NUCLEI_ENV_36}/bin/activate"
python3.6 pipeline/8_find_sub_image_patch_with_highest_nuclei_density_in_high_resolution_image_patch.py \
  -i $S8_NUCLEI_SEGMENTOR_INPUT_DIRECTORY_PATH \
  -o $S8_NUCLEI_SEGMENTOR_OUTPUT_DIRECTORY_PATH

