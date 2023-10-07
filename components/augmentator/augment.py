import cv2
from augraphy.default.pipeline import pipeline_archetype1, pipeline_archetype2, pipeline_archetype3, \
    pipeline_archetype7, pipeline_archetype6, pipeline_archetype8, pipeline_archetype9, \
    pipeline_archetype10, pipeline_archetype11, pipeline_archetype4

pipeline_fns = [pipeline_archetype1, pipeline_archetype2, pipeline_archetype3, pipeline_archetype4, pipeline_archetype6,
                pipeline_archetype7, pipeline_archetype8, pipeline_archetype9, pipeline_archetype10,
                pipeline_archetype11]
# pipeline_fns = [pipeline_archetype1, pipeline_archetype2]
filepath = "/Users/ssdn/PycharmProjects/Artificial-document-generator/data/output/images/receipt/"
img_name = "image0.png"
image = cv2.imread(filepath + img_name)

count = 0
for fn in pipeline_fns:
    pipeline = fn()
    data = pipeline(image)
    aug_img = img_name[:-4] + "_" + str(count) + img_name[-4:]
    # data = cv2.resize(data, up_points, interpolation= cv2.INTER_LINEAR)
    cv2.imwrite(filepath + "augmented/" + aug_img, data)
    count += 1
