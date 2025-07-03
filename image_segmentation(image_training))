import os 
import numpy as np 
from tensorflow.keras.preprocessing.image import load_img, img_to_array 
from tqdm import tqdm 
 
cityscapes_colors = { 
    0: [0, 0, 0], 1: [128, 64, 128], 2: [244, 35, 232], 3: [70, 70, 70], 4: [102, 102, 156], 
    5: [190, 153, 153], 6: [153, 153, 153], 7: [250, 170, 30], 8: [220, 220, 0], 9: [107, 142, 35], 
    10: [152, 251, 152], 11: [70, 130, 180], 12: [220, 20, 60], 13: [255, 0, 0], 14: [0, 0, 142], 
    15: [0, 0, 70], 16: [0, 60, 100], 17: [0, 80, 100], 18: [0, 0, 230], 19: [119, 11, 32] 
} 
 
def rgb_to_onehot(rgb_image, colormap=cityscapes_colors): 
    num_classes = len(colormap) 
    shape = rgb_image.shape[:2] + (num_classes,) 
    encoded_image = np.zeros(shape, np.int8) 
    for i, cls in enumerate(colormap.values()): 
        matches = np.all(rgb_image == np.array(cls).reshape(1, 1, 3), axis=-1).astype(int) 
        encoded_image[:, :, i] = matches 
    return encoded_image 
 
def get_image_files(directory): 
    image_files = [] 
    for dirpath, _, filenames in os.walk(directory): 
        for filename in filenames: 
            if filename.endswith(('.png', '.jpg', '.jpeg')): 
                image_files.append(os.path.relpath(os.path.join(dirpath, filename), directory)) 
    return image_files 
 
def load_dataset(image_files, images_dir, masks_dir, img_height, img_width): 
    images, masks = [], [] 
    for image_file in tqdm(image_files): 
        img_path = os.path.join(images_dir, image_file) 
        mask_path = os.path.join(masks_dir, image_file.replace("leftImg8bit", "gtFine_color")) 
        try: 
            img = load_img(img_path, target_size=(img_height, img_width)) 
            img_array = img_to_array(img) / 255.0 
            images.append(img_array) 
  
            mask_img = load_img(mask_path, target_size=(img_height, img_width), color_mode="rgb") 
            mask_img_array = img_to_array(mask_img) 
            mask_img_array = rgb_to_onehot(mask_img_array, cityscapes_colors) 
            masks.append(mask_img_array) 
        except Exception as e: 
            print(f"Error loading image or mask for {image_file}: {e}") 
    return np.array(images), np.array(masks) 
