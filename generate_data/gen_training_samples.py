import random
import cv2
from my_voc import my_voc
import numpy as np
import os
import sys

def box_area(xmin, ymin, xmax, ymax):
	return (float(xmax) - float(xmin)) * (float(ymax) - float(ymin))

def mask_img(box):
	xmin, ymin, xmax, ymax = box
	satified = False
	while not satified:
		mask_xmin, mask_xmax = sorted(np.random.randint(xmin, xmax+1, 2))
		mask_ymin, mask_ymax = sorted(np.random.randint(ymin, ymax+1, 2))
		ratio = box_area(mask_xmin, mask_ymin, mask_xmax, mask_ymax) / \
			box_area(xmin, ymin, xmax, ymax) 
		if ratio >= 0.2 and ratio < 0.7:
			satified = True
	mask = [mask_xmin, mask_ymin, mask_xmax, mask_ymax]
	return mask

def black_patch(img, annot):
	# for every object
	# random mask black patch
	boxes = annot['boxes']
	gt_classes = annot['gt_classes']
	for (box, cls) in zip(boxes, gt_classes):
		if not cls == 15:
			continue
		if random.random() > 0.0:
			mask = mask_img(box)
			cv2.rectangle(img, (mask[0], mask[1]), (mask[2], mask[3]), (104,117,123), -1)
	return 
	# return masked image

if __name__ == '__main__':
	random.seed(100)
	voc_dir = os.path.join(sys.path[0], '../dataset/VOC2012')
	voc = my_voc(voc_dir)
	# get all images 
	img_list = voc._list_imgs()
	# get all annotations
	annot_list = voc._list_annots()
	assert len(img_list) == len(annot_list)
	# iterate every image
	for ix, (img_file, annot_file) in enumerate(zip(img_list, annot_list)):
		if ix >= 20:
			break
		img = cv2.imread(img_file)
		# get annotations 
		annot = voc._read_annot(annot_file)
		# generate black patched image
		black_patch(img, annot)

		save_file = os.path.join(os.path.join(voc_dir, 'masked'), os.path.basename(img_file))
		# save_file = os.path.join(sys.path[0], os.path.basename(img_file))
		cv2.imwrite(save_file, img)

	

