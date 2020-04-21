#!/bin/bash

###################################
#             INPUTS              #
###################################

S0_VIRTUAL_ENV_27=${1?Error: no virtual environment directory path given}
S0_VIRTUAL_ENV_36=${2?Error: no virtual environment directory path given}
S0_VIRTUAL_NUCLEI_ENV_36=${3?Error: no virtual environment directory path given}
S0_INPUT_DIRECTORY_PATH=${4?Error: no input directory path given}
S0_OUTPUT_DIRECTORY_PATH=${5?Error: no output directory path given}

###################################
#             CONFIG              #
###################################

# 1_split_svs_images_to_image_patches
#####################################
S1_SPLIT_SVS_S0_INPUT_DIRECTORY_PATH=${S0_INPUT_DIRECTORY_PATH}
S1_SPLIT_SVS_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/1_split_svs_images_to_image_patches"
S1_RESOLUTION_LEVEL=2
S1_OVERLAP_PERCENTAGE=75
S1_WINDOW_SIZE=800

# 2_preprocess_image_patches
#####################################
S2_PREPROCESS_IMAGE_PATCHES_INPUT_DIRECTORY_PATH=${S1_SPLIT_SVS_OUTPUT_DIRECTORY_PATH}
S2_PREPROCESS_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/2_preprocess_image_patches"
S2_FIRST_CENTERMOST_CROP_SIZE=512
S2_DOWNSCALED_SIZE=256
S2_SECOND_CENTERMOST_CROP_SIZE=227

# 3_predict_saliency_for_image_patches
#####################################
S3_PREDITCT_SALIENCY_INPUT_DIRECTORY_PATH=${S2_PREPROCESS_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH}
S3_PREDITCT_SALIENCY_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/3_predict_saliency_for_image_patches"

# 4_create_saliency_visualization
#####################################
S4_CREATE_SALIENCY_VISUALIZATION_SVS_INPUT_DIRECTORY_PATH=${S0_INPUT_DIRECTORY_PATH}
S4_CREATE_SALIENCY_VISUALIZATION_CSV_INPUT_DIRECTORY_PATH=${S3_PREDITCT_SALIENCY_OUTPUT_DIRECTORY_PATH}
S4_CREATE_SALIENCY_VISUALIZATION_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/4_create_saliency_visualization"
S4_CREATE_SALIENCY_ACCURACY_PERCENTAGE_THRESHOLD=0.998

# 5_convert_salient_image_patches_to_high_resolution_image_patches
#####################################
S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_SVS_INPUT_DIRECTORY=${S0_INPUT_DIRECTORY_PATH}
S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_CSV_INPUT_DIRECTORY=${S3_PREDITCT_SALIENCY_OUTPUT_DIRECTORY_PATH}
S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/5_create_high_resolution_image_patches"
S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_TARGET_RESOLUTION_LEVEL=0
S5_CREATE_HIGH_RESOLUTION_IMAGE_OVERLAP_PERCENTAGE=0
S5_CREATE_HIGH_RESOLUTION_IMAGE_WINDOW_SIZE=800

# 6_preprocess_high_resolution_image_patches
#####################################
S6_PREPROCESS_HIGH_RESOLUTION_IMAGE_PATCHES_INPUT_DIRECTORY_PATH=${S5_CREATE_HIGH_RESOLUTION_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH}
S6_PREPROCESS_HIGH_RESOLUTION_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/6_preprocess_high_resolution_image_patches"
S6_HIGH_RESOLUTION_IMAGE_PATCH_DOWNSCALED_SIZE=512

# 7_reorganize_directories_for_segmentor
#####################################
S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_INPUT_DIRECTORY_PATH=${S6_PREPROCESS_HIGH_RESOLUTION_IMAGE_PATCHES_OUTPUT_DIRECTORY_PATH}
S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/7_reorganize_directories_for_segmentor"

# 8_find_sub_image_patch_with_highest_nuclei_density_in_high_resolution_image_patch
#####################################
S8_NUCLEI_SEGMENTOR_INPUT_DIRECTORY_PATH=${S7_REORGANIZE_DIRECTORIES_FOR_SEGMENTOR_OUTPUT_DIRECTORY_PATH}
S8_NUCLEI_SEGMENTOR_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/8_find_sub_image_patch_with_highest_nuclei_density_in_high_resolution_image_patch"

# 9_find_sub_image_patch_with_highest_nuclei_density
#####################################
S9_FIND_SUB_IMAGE_PATCH_WITH_HIGHEST_NUCLEI_DENSITY_INPUT_DIRECTORY_PATH=${S8_NUCLEI_SEGMENTOR_OUTPUT_DIRECTORY_PATH}
S9_FIND_SUB_IMAGE_PATCH_WITH_HIGHEST_NUCLEI_DENSITY_OUTPUT_DIRECTORY_PATH="${S0_OUTPUT_DIRECTORY_PATH}/9_find_sub_image_patch_with_highest_nuclei_density"
