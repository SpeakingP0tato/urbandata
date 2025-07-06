import os 
import numpy as np 
from tensorflow.keras.preprocessing import image 
import matplotlib.pyplot as plt 
from tqdm import tqdm 
 
cityscapes_colors = { 
    0: [0, 0, 0], 1: [128, 64, 128], 2: [244, 35, 232], 3: [70, 70, 70], 4: [102, 102, 156], 
    5: [190, 153, 153], 6: [153, 153, 153], 7: [250, 170, 30], 8: [220, 220, 0], 9: [107, 142, 35], 
    10: [152, 251, 152], 11: [70, 130, 180], 12: [220, 20, 60], 13: [255, 0, 0], 14: [0, 0, 142], 
    15: [0, 0, 70], 16: [0, 60, 100], 17: [0, 80, 100], 18: [0, 0, 230], 19: [119, 11, 32] 
} 
 
def apply_color_map(segmentation_result, colormap=cityscapes_colors): 
    color_image = np.zeros(segmentation_result.shape + (3,), dtype=np.uint8) 
    for label, color in colormap.items(): 
        color_image[segmentation_result == label] = color 
    return color_image 
 
def get_image_files(folder): 
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))] 
 
def segment_and_save_images(input_folder, output_folder, model, img_height, img_width): 
    if not os.path.exists(output_folder): 
        os.makedirs(output_folder) 
 
    image_files = get_image_files(input_folder) 
    for image_file in tqdm(image_files): 
        img_path = os.path.join(input_folder, image_file) 
        img = image.load_img(img_path, target_size=(img_height, img_width)) 
        img_array = image.img_to_array(img) / 255.0 
        img_array = np.expand_dims(img_array, axis=0) 
 
        segmentation_result = np.argmax(model.predict(img_array), axis=-1)[0].astype(np.int32) 
        segmented_image_colored = apply_color_map(segmentation_result) 
 
        output_image_path = os.path.join(output_folder, image_file) 
        plt.imsave(output_image_path, segmented_image_colored)
