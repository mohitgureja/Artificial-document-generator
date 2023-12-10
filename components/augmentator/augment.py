import glob
import os
import random

import cv2
from augraphy.default.pipeline import pipeline_archetype1, pipeline_archetype2, pipeline_archetype3, \
    pipeline_archetype7, pipeline_archetype6, pipeline_archetype8, pipeline_archetype9, \
    pipeline_archetype10, pipeline_archetype11, pipeline_archetype4

pipelines = [pipeline_archetype1, pipeline_archetype2, pipeline_archetype3, pipeline_archetype4, pipeline_archetype6,
             pipeline_archetype7, pipeline_archetype8, pipeline_archetype9, pipeline_archetype10,
             pipeline_archetype11]
# pipeline_fns = [pipeline_archetype1, pipeline_archetype2]
# pipeline_fns = random.sample(pipeline_fns, 3)
filepath = "/Users/ssdn/PycharmProjects/Artificial-document-generator/data/output/images/invoices"
augment_filepath = "/Users/ssdn/PycharmProjects/Artificial-document-generator/data/output/images/invoice/augmented/"
image_files = glob.glob(os.path.join(filepath, "*.png"))
for img in image_files:
    pipeline_fns = random.sample(pipelines, 3)
    image = cv2.imread(img)
    count = 0
    for fn in pipeline_fns:
        pipeline = fn()
        data = pipeline(image)
        image_name = os.path.basename(img)
        aug_img = image_name[:-4] + "_" + str(count) + image_name[-4:]
        print(aug_img)
        # data = cv2.resize(data, up_points, interpolation= cv2.INTER_LINEAR)
        if not cv2.imwrite(os.path.join(augment_filepath, aug_img), data):
            raise Exception
        count += 1
