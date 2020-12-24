import cv2
import numpy as np

def make_mask(filename):
	mask_image = cv2.imread(filename)
	mask = mask_image.astype(np.bool)
	return mask

def apply_mask(image, mask):
	w, h, _ = image.shape
	mask_w, mask_h, _ = mask.shape
	if w != mask_w or h != mask_h:
		mask = cv2.resize(mask, dsize=(w, h))

	return image * mask

if __name__ == "__main__":
	mask = make_mask('mask.png')
	image = cv2.imread('test.png')
	masked_image = apply_mask(image, mask)
	cv2.imwrite('masked_image.png', masked_image)