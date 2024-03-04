import glob
import os
import random

import cv2
from augraphy.default.pipeline import pipeline_archetype1, pipeline_archetype2, pipeline_archetype3, \
    pipeline_archetype7, pipeline_archetype6, pipeline_archetype8, pipeline_archetype9, \
    pipeline_archetype10, pipeline_archetype11, pipeline_archetype4
from loguru import logger

pipelines = [pipeline_archetype1, pipeline_archetype2, pipeline_archetype3, pipeline_archetype4, pipeline_archetype6,
             pipeline_archetype7, pipeline_archetype8, pipeline_archetype9, pipeline_archetype10,
             pipeline_archetype11]


# pipeline_fns = [pipeline_archetype1, pipeline_archetype2]
# pipeline_fns = random.sample(pipeline_fns, 3)
# filepath = "/Users/ssdn/PycharmProjects/Artificial-document-generator/data/output/images/resume"
# augment_filepath = "/Users/ssdn/PycharmProjects/Artificial-document-generator/data/output/images/resume/augmented/"

def augment_dataset(directory_path):
    logger.info("\n------------------- Starting Augmentation -------------------\n")
    logger.info("It might take a few minutes.")
    augment_filepath = os.path.dirname(os.path.normpath(directory_path)) + os.path.sep + "augmented"
    if not os.path.exists(augment_filepath):
        os.makedirs(augment_filepath)

    image_files = glob.glob(os.path.join(directory_path, "*.png"))
    count = 0
    for img in image_files:
        pipeline_fns = random.sample(pipelines, 1)
        image = cv2.imread(img)
        for fn in pipeline_fns:
            pipeline = fn()
            data = pipeline(image)
            image_name = os.path.basename(img)
            aug_img = image_name[:-4] + "_" + str(count) + image_name[-4:]
            if not cv2.imwrite(os.path.join(augment_filepath, aug_img), data):
                raise Exception
            count += 1
    logger.info(f'Augmentation completed for {count} files')
    return augment_filepath
